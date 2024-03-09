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
        user = os.getenv("POSTGRES_USER", "postgresuser")
        password = os.getenv("POSTGRES_PASSWORD", "postgrespassword")
        host = os.getenv("DB_URL", "localhost")
        port = os.getenv("DB_PORT", "5432")

        conn = psycopg2.connect(
            dbname='twitty',
            user=user,
            password=password,
            host=host
            # port=port
        )
        cur = conn.cursor()

        # Load and preprocess data
        twitter_df = pd.read_csv('tweets_df.csv', delimiter='	')
        twitter_df = twitter_df.replace({np.nan: None})

        tweets_paritioned_by_word = twitter_df.explode('parsed_content')
        tweets_paritioned_by_word = tweets_paritioned_by_word.dropna(subset=["parsed_content"])

        twitter_df['parsed_content'] = twitter_df['parsed_content'].apply(convert_to_list)

        raw_twitter_df = list(twitter_df[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))

        print('starting with tables creation')

        # tweets_by_likes
        insert_tweets_by_likes = """INSERT INTO tweets_by_likes (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_likes, raw_twitter_df)

        print('Finished creating tweets_by_likes')

        # tweets_by_share
        insert_tweets_by_share = """INSERT INTO tweets_by_share (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_share, raw_twitter_df)

        print('Finished creating tweets_by_share')

        # user_tweets
        insert_user_tweets = """INSERT INTO user_tweets (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_user_tweets, raw_twitter_df)

        print('Finished creating user_tweets')

        # user_tweets
        raw_tweets_paritioned_by_word = list(tweets_paritioned_by_word[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))
        insert_tweets_by_word = """INSERT INTO tweets_by_word (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        execute_values(cur, insert_tweets_by_word, raw_tweets_paritioned_by_word)

        print('Finished creating tweets_by_word')

        cur.execute("""CREATE TABLE db_digested (id INT PRIMARY KEY);""")
        cur.execute("""INSERT INTO db_digested(id) VALUES (1);""")

        # Commit the transaction
        conn.commit()
        print('Finished creating all tables')

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
