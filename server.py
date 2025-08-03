import json
import logging
import os
import tempfile
from contextlib import asynccontextmanager

import numpy as np
import requests
import soundfile as sf
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from kokoro import KPipeline
from pydantic import BaseModel
from starlette.requests import Request
from transformers import pipeline

from prompts import map_prompts_to_params

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


language_map = {"en": "a", "es": "e"}
speaker_map = {"en": "af_heart", "es": "em_santa"}


def load_models(app: FastAPI) -> FastAPI:
    gemma = pipeline("image-text-to-text", model="google/gemma-3n-E2B-it")
    app.gemma = gemma
    return app


def generate_text_direct(prompt: str, gemma):
    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
    ]
    response = gemma(text=messages, temperature=0.0, top_p=0.99, max_new_tokens=2048)
    return response[0]["generated_text"][-1]["content"]


def cleanup_temp_file(file_path: str):
    """Clean up temporary file after response is sent"""
    try:
        os.unlink(file_path)
    except OSError:
        pass


def text_to_audio_chunks(text, voice="af_heart", language="a"):
    pipeline = KPipeline(lang_code=language)
    generator = pipeline(text, voice=voice)
    audios = [audio for (gs, ps, audio) in generator]
    return audios


def concat_chunks(audios, samplerate=24000, silence_dur=0.3):
    # Convert PyTorch tensors to NumPy arrays
    audio_arrays = [
        audio.numpy() if hasattr(audio, "numpy") else audio for audio in audios
    ]

    if not audio_arrays:
        return np.array([])  # Return empty array if no audio chunks

    silence = np.zeros(int(samplerate * silence_dur), dtype=audio_arrays[0].dtype)
    # Insert silence between all but last
    chunks = sum([[chunk, silence] for chunk in audio_arrays[:-1]], []) + [
        audio_arrays[-1]
    ]
    return np.concatenate(chunks)


def get_audio(text: str, language: str):
    voice = speaker_map.get(language, "af_heart")
    language = language_map.get(language, "a")
    audios = text_to_audio_chunks(text, voice=voice, language=language)
    final_audio = concat_chunks(audios)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, final_audio, 24000)
    tmp.close()
    return tmp.name


def generate_text(prompt: str):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "Emotions API",
            "X-Title": "Emotions API",
        },
        data=json.dumps(
            {
                "model": "google/gemma-3n-e4b-it:free",
                "temperature": 0.0,
                "max_tokens": 2048,
                "top_p": 0.99,
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
    )
    response_json = response.json()
    answer = response_json["choices"][0]["message"]["content"]
    return answer, response_json


def generate_audio(text: str, language: str) -> FileResponse:
    audio_path = get_audio(text, language)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(cleanup_temp_file, audio_path)

    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename="generated_audio.wav",
        background=background_tasks,
    )


class InputLoadT2A(BaseModel):
    text: str
    language: str


class InputLoadP2T(BaseModel):
    text: str


class ResponseLoadP2T(BaseModel):
    text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app = load_models(app=app)
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"server": "running"}


@app.post("/genaudio/")
async def receive(input_load: InputLoadT2A, request: Request) -> FileResponse:
    return generate_audio(input_load.text, input_load.language)


@app.post("/gentext/")
async def gen_text(input_load: InputLoadP2T, request: Request) -> ResponseLoadP2T:
    gemma = request.app.gemma
    text = generate_text_direct(input_load.text, gemma)
    return ResponseLoadP2T(text=text)


@app.post("/gentextopenrouter/")
async def gen_text(input_load: InputLoadP2T, request: Request) -> ResponseLoadP2T:
    text, _ = generate_text(input_load.text)
    return ResponseLoadP2T(text=text)


@app.post("/genemotion/")
async def gen_emotion(input_load: InputLoadT2A, request: Request) -> FileResponse:
    text, _ = generate_text(input_load.text)
    return generate_audio(text, input_load.language)


@app.post("/genemotionfast/")
async def gen_emotion_fast(input_load: InputLoadT2A, request: Request) -> FileResponse:
    logger.info(
        f"Received request at FASTgen for text: {input_load.text}, language: {input_load.language}"
    )
    return get_preloaded_audio(input_load.text, input_load.language)


def get_preloaded_audio(prompt: str, language: str) -> FileResponse:
    request_params = map_prompts_to_params[prompt]
    audio_file = f"preloaded_audio/audio_{request_params['emotion']}_{language}.mp3"
    return FileResponse(
        path=audio_file,
        media_type="audio/mp3",
        filename=f"audio_{request_params['emotion']}_{language}.mp3",
    )
