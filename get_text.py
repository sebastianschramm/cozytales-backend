import json

import requests

from prompts import emotion_prompts, story_prompts

url = "http://0.0.0.0:6002/gentext"


languages = ["en", "es"]  # en, es
emotions = ["anxiety", "sadness", "anger"]


# for language in languages:
#     for emotion in emotions:
#         prompt = emotion_prompts[emotion][language]
#         response = requests.post(url, json={"text": prompt})

#         with open(f'preloaded_texts/text_{emotion}_{language}.json', 'w') as f:
#             json.dump(response.json(), f , indent=2, ensure_ascii=False)


for language in languages:
    prompt = story_prompts[language]
    response = requests.post(url, json={"text": prompt})

    with open(f"preloaded_texts/text_story_{language}.json", "w") as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
