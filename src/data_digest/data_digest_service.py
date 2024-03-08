import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np
import ast
import os


def convert_to_list(row):
    try:
        return ast.literal_eval(row)
    except ValueError:
        return []



def digest_data():
    conn = None
    cur = None
    try:
        # Database connection parameters from environment variables
        # dbname = os.getenv("POSTGRES_DB", "twitty")
        dbname = 'twitty'  # The database name
        user = 'postgresuser'  # The database user
        password = 'postgrespassword'  # The user's password
        host = 'postgres-service'  # Host address of the PostgreSQL server
        port = '5432'  # Port number


        # Connect to the database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Load and preprocess data
        twitter_df = pd.read_csv('./tweets_df.csv', delimiter='	')
        twitter_df = twitter_df.replace({np.nan: None})

        tweets_paritioned_by_word = twitter_df.explode('parsed_content')
        tweets_paritioned_by_word = tweets_paritioned_by_word.dropna(subset=["parsed_content"])

        twitter_df['parsed_content'] = twitter_df['parsed_content'].apply(convert_to_list)

        raw_twitter_df = list(twitter_df[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))

        # tweets_by_likes
        insert_tweets_by_likes = """INSERT INTO tweets_by_likes (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_likes, raw_twitter_df)

        # tweets_by_share
        insert_tweets_by_share = """INSERT INTO tweets_by_share (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_share, raw_twitter_df)

        # user_tweets
        insert_user_tweets = """INSERT INTO user_tweets (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_user_tweets, raw_twitter_df)

        # user_tweets
        raw_tweets_paritioned_by_word = list(tweets_paritioned_by_word[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))
        insert_tweets_by_word = """INSERT INTO tweets_by_word (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_word, raw_tweets_paritioned_by_word)

        # Commit the transaction
        conn.commit()

    except Exception as e:
        # Rollback the transaction in case of error
        if conn is not None:
            conn.rollback()
        print(f"An error occurred: {e}")
        # Optionally, re-raise the exception if you want the error to propagate
        raise

    finally:
        # Close the cursor and connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    digest_data()
