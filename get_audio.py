import json
import shutil

from server import generate_audio

languages = ["en", "es"]  # en, es
emotions = ["anxiety", "sadness", "anger"]


def load_text(language: str, emotion: str = None) -> str:
    file = (
        f"preloaded_texts/text_{emotion}_{language}.json"
        if emotion
        else f"preloaded_texts/text_story_{language}.json"
    )
    with open(file, "r") as f:
        data = json.load(f)
    return data["text"]


for language in languages:
    for emotion in emotions:
        text = load_text(language, emotion)
        audio = generate_audio(text, language)
        filename = f"preloaded_audio/audio_{emotion}_{language}.wav"
        shutil.copyfile(audio.path, filename)

    text = load_text(language, None)
    audio = generate_audio(text, language)
    filename = f"preloaded_audio/audio_story_{language}.wav"
    shutil.copyfile(audio.path, filename)
