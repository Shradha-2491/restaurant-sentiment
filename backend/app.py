from flask import Flask, request, jsonify
from joblib import load
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

model = load("sentiment_classifier_model_modified.joblib")
tfidf_vectorizer = load("tfidf_vectorizer_modified.joblib")

# Load NLTK stopwords
# Stopwords are installed during the Docker image build.
ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')

def preprocess_review(review):
    # Remove non-letters
    review = re.sub("[^a-zA-Z]", " ", review)
    # Convert to lowercase
    review = review.lower()
    # Split into words
    review = review.split()
    # Stemming and removing stopwords
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    # Join back
    review = " ".join(review)
    return review

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    review = data['review']
    review = preprocess_review(review)
    review_transformed = tfidf_vectorizer.transform([review]).toarray()
    prediction = model.predict(review_transformed)
    return jsonify(sentiment=int(prediction[0]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)