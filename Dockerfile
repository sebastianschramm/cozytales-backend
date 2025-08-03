FROM python:3.11-slim

RUN useradd -m -u 1000 user

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

RUN python -m spacy download en_core_web_sm

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]