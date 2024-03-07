from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/digest', methods=['POST'])
def digest():
    tokens = request.form['tokens']
    source = request.form.get('source')
    # Add your data processing logic here based on the tokens and selected source
    response = requests.get(f"http://backend-service:5000/get_tweet_sentiment?tweet_id={tokens}")

    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
