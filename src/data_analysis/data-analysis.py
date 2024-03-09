from flask import Flask, jsonify, request
from cassandra.cluster import Cluster

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

@app.route('/')
def home():
    return "home page"

@app.route('/get_tweet')
def get_tweet(tweet_id = None):
    try:
        if not tweet_id:
            tweet_id = request.args.get('tweet_id')
            if not tweet_id:
                return jsonify({'error': 'Query parameter is missing'}), 400

        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
        session.set_keyspace('twitter')

        
        statement = f"SELECT tweet FROM tweets where tweet_id = '{tweet_id}';"
        result_set = session.execute(statement)._current_rows
        rows = list(result_set)

        tweet = rows[0][0]

        # Return the query result as JSON
        return tweet, 200

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500



@app.route('/get_tweet_sentiment')
def get_tweet_sentiment():
    dict = {}
    tweet_id = request.args.get('tweet_id')
    if not tweet_id:
        return jsonify({'error': 'Query parameter is missing'}), 400
    
    tweet, status_code = get_tweet(tweet_id=tweet_id)
    if status_code != 200:
        return tweet, status_code
    else:
        dict["tweet"] = tweet
        preprocess_tweet = preprocess_text(tweet)
        sentiment = get_sentiment(preprocess_tweet)
        dict["sentiment"] = sentiment
        return jsonify(dict), 200
    
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text

def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sentiment = 1 if scores['pos'] > 0.3 else 0
    return sentiment

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)