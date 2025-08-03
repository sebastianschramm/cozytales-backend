import json
import shutil

from server import generate_audio

text = """Every child deserves a comforting voice at bedtime…
or a gentle story to help them through big feelings.
Cozy Tales is an AI-powered storytelling app that supports children through emotions like anxiety, sadness, or anger — when they need it most.
Using Google’s Gemma 3n language model, Cozy Tales creates culturally relevant stories, tailored for children aged 4 to 7.
Stories are available in English and Spanish, adapted for different cultures — with more to come.
And with the lightweight Kokoro-82M voice model, each story is read aloud with warmth and clarity.
Whether it's bedtime... or a moment of emotional need...
Cozy Tales brings comfort, connection, and care — through AI.
Because sometimes, all a child needs… is a good story."""


text = """Every child deserves a comforting voice at bedtime…
or a gentle story to help them feel safe, seen, and soothed during life’s big emotions.
Cozy Tales is an Artificial Intelligence-powered storytelling app designed to support children through feelings like anxiety, sadness, or anger — right in the moments they need it most.
Moments that can feel overwhelming for little hearts… especially when no grown-up is there to help them make sense of it all.
Built using Google’s Gemma 3n language model, Cozy Tales creates emotionally intelligent, culturally meaningful stories tailored for children aged 4 to 7.
Stories that speak their language — literally — with offerings in both English and Spanish, and cultural adaptations to reflect the diverse families and backgrounds we serve.
And with the lightweight Kokoro-82M voice model, each story is read aloud with warmth, clarity, and a tone that feels like a gentle hug.
Because sometimes the tears come before bedtime…
Sometimes worries show up in the middle of the day…
And sometimes, big emotions arrive when no parent, caregiver, or teacher is nearby.
In those moments — when a child might otherwise face their feelings alone — Cozy Tales becomes a quiet companion.
A steady voice.
A story that understands.
Helping children name their feelings, breathe through them, and feel just a little more okay.
Whether it’s a meltdown after preschool, a lonely afternoon, or a restless night…
Cozy Tales is always just a tap away — bringing comfort, connection, and care through the power of story and AI.
Because sometimes, all a child needs… is a good story told with heart — exactly when they need it most."""


text = """Every child deserves a comforting voice at bedtime…
or a gentle story to help them feel safe, seen, and soothed during life’s big emotions.
Cozy Tales is an Artificial Intelligence-powered storytelling app designed to support children through feelings like anxiety, sadness, or anger — right in the moments they need it most.
Moments that can feel overwhelming for little hearts… especially when no grown-up is there to help them make sense of it all.
Built using Google’s Gemma 3n language model, Cozy Tales creates emotionally intelligent, culturally meaningful stories tailored for children aged 4 to 7.
Stories that speak their language — literally — with offerings in both English and Spanish, and cultural adaptations to reflect the diverse families and backgrounds we serve.
And with the lightweight Kokoro-82M voice model, each story is read aloud with warmth, clarity, and a tone that feels like a gentle hug.
Because sometimes the tears come before bedtime…
Sometimes worries show up in the middle of the day…
And sometimes, big emotions arrive when no parent, caregiver, or teacher is nearby.
In those moments — when a child might otherwise face their feelings alone — Cozy Tales becomes a quiet companion.
A steady voice.
A story that understands.
Helping children name their feelings, breathe through them, and feel just a little more okay.
Whether it’s a meltdown after preschool, a lonely afternoon, or a restless night…
Cozy Tales is always just a tap away — bringing comfort, connection, and care through the power of story and AI.
Because sometimes, all a child needs… is a good story told with heart — exactly when they need it most."""

text = """Every child deserves a comforting voice at bedtime…
or a gentle story to help them feel safe, seen, and soothed during life’s big emotions.
Cozy Tales is an Artificial Intelligence-powered storytelling app that supports children through feelings like anxiety, sadness, or anger — right when they need it most.
Moments that can feel overwhelming for little hearts… especially when no grown-up is there to help them make sense of it all.
Built with Google’s Gemma 3n language model, Cozy Tales creates emotionally intelligent, culturally meaningful stories for kids aged 4 to 7.
Stories that speak their language — with options in English and Spanish, and cultural adaptations for the diverse families we serve.
And with the Kokoro-82M voice model, each story is read aloud with warmth, clarity, and a tone that feels like a gentle hug."""

text = """Because sometimes the tears come before bedtime…
Sometimes worries show up in the middle of the day…
And sometimes, big emotions arrive when no parent, caregiver, or teacher is nearby.

In those moments — when a child might otherwise face their feelings alone — Cozy Tales becomes a quiet companion.
A steady voice.
A story that understands.

Helping children name their feelings, breathe through them, and feel just a little more okay.

Whether it’s a meltdown after preschool, a lonely afternoon, or a restless night…
Cozy Tales is always just a tap away — bringing comfort, connection, and care through the power of story and AI.

Because sometimes, all a child needs… is a good story told with heart — exactly when they need it most."""

text = """Because sometimes the tears come before bedtime…
Sometimes worries show up in the middle of the day…
And sometimes, big emotions arrive when no parent, caregiver, or teacher is nearby.
"""

text = """In those moments — when a child might otherwise face their feelings alone — Cozy Tales becomes a quiet companion.
A steady voice. A story that understands.
Helping children name their feelings, breathe through them, and feel just a little more okay.
Whether it’s a meltdown after preschool, a lonely afternoon, or a restless night…
Cozy Tales is always just a tap away — bringing comfort, connection, and care through the power of story and AI.

Because sometimes, all a child needs… is a good story told with heart — exactly when they need it most..."Cozy Tales"!"""

audio = generate_audio(text, "en")
filename = f"audio_voicover_en_third.wav"
shutil.copyfile(audio.path, filename)
