from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/digest', methods=['POST'])
def digest():
    tokens = request.form['tokens']
    # Add your data processing logic here based on the tokens and selected source
    #response = requests.get(f"http://backend-service:5000/get_tweet_sentiment?tweet_id={tokens}")
    response = requests.get(f"http://127.0.0.1:5000/get_tweet_sentiment_visualization?tokens={tokens}", stream=True)

    return Response(response.content, content_type=response.headers['Content-Type'])


@app.route('/tweets_distribution', methods=['POST'])
def tweets_distribution():
    # Add your data processing logic here based on the tokens and selected source
    response = requests.get(f"http://127.0.0.1:5000/tweets_distribution", stream=True)
    
    # Return the image response directly
    return Response(response.content, content_type=response.headers['Content-Type'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
