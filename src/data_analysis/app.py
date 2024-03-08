from flask import Flask, jsonify, request, send_file
# import psycopg2
# import psycopg2.extras

import io

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import matplotlib.pyplot as plt

app = Flask(__name__)



def get_db_connection():
    conn = psycopg2.connect(
        host='postgres-service', 
        dbname='twitty', 
        user='postgresuser',  
        password='postgrespassword',  
        port='5432'
    )
    return conn


def get_tweets_distribution():
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT author, COUNT(tweet_id) as tweet_count FROM user_tweets GROUP BY author;")
    author_data = cur.fetchall()
    conn.close()
    '''

    # mock data for tests
    author_data = [
        ('AuthorA', 120),
        ('AuthorB', 90),
        ('AuthorC', 150),
        ('AuthorD', 30),
        ('AuthorE', 60)
    ]

    authors = [row[0] for row in author_data]
    tweet_counts = [row[1] for row in author_data]

    plt.figure(figsize=(10, 6))
    plt.bar(authors, tweet_counts, color='skyblue')
    plt.xlabel('Authors')
    plt.ylabel('Number of Tweets')
    plt.title('Distribution of Tweets by Author')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf



@app.route('/')
def home():
    return "home page"


@app.route('/tweets_distribution')
def tweets_distribution():
    try:
        img = get_tweets_distribution()
        return send_file(img, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/get_tweet')
def get_tweet(tweet_id=None):
    try:
        if not tweet_id:
            tweet_id = request.args.get('tweet_id')
            if not tweet_id:
                return jsonify({'error': 'Query parameter is missing'}), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Example query from tweets_by_likes. Adjust as necessary for your application logic
        cur.execute("SELECT content FROM tweets_by_likes WHERE tweet_id = %s;", (tweet_id,))
        row = cur.fetchone()

        if row:
            tweet = row['content']  # Ensure column name matches your schema
            return jsonify(tweet=tweet), 200
        else:
            return jsonify({'error': 'Tweet not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/get_tweet_sentiment')
def get_tweet_sentiment():
    author_name = request.args.get('author')
    if not author_name:
        return jsonify({'error': 'Query parameter "author" is missing'}), 400
    
    try:

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Query all tweets from the specified author
        cur.execute("SELECT content FROM user_tweets WHERE author = %s;", (author_name,))
        tweets = cur.fetchall()

        if not tweets:
            return jsonify({'error': 'No tweets found for this author'}), 404
        
        sentiments = []
        for tweet in tweets:
            processed_tweet = preprocess_text(tweet['content'])
            sentiment = get_sentiment(processed_tweet)
            sentiments.append({'tweet': tweet['content'], 'sentiment': sentiment})

        return jsonify(sentiments), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
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
