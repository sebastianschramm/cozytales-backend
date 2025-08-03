import os

from pydub import AudioSegment


def convert_wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")


for file in os.listdir("preloaded_audio"):
    if file.endswith(".wav"):
        wav_file = os.path.join("preloaded_audio", file)
        mp3_file = os.path.join("preloaded_audio", file.replace(".wav", ".mp3"))
        convert_wav_to_mp3(wav_file, mp3_file)
        print(f"Converted {wav_file} to {mp3_file}")
