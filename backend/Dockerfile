FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK stopwords at build time, not at container startup
RUN python -c "import nltk; nltk.download('stopwords', download_dir='/usr/share/nltk_data')"

COPY app.py .
COPY sentiment_classifier_model_modified.joblib .
COPY tfidf_vectorizer_modified.joblib .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
