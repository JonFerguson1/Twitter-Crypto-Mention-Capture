from kafka import KafkaConsumer
import mysql.connector
from database import cursor, user, pw, host, db
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

TOPIC = 'crypto'

DB_NAME = 'crypto_mentions'
engine = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}/{}'.format(user, pw, host, DB_NAME))

cursor.execute("USE {}".format(DB_NAME))

print("Connecting to Kafka")
consumer = KafkaConsumer(TOPIC)
print("Connected to Kafka")
print(f"Reading messages from the topic {TOPIC}")

for msg in consumer:

    message = msg.value.decode("utf-8")

    (tweet_time, user, coin, mention_count, price_at_tweet) = message.split(",")
    
    tweet_time = datetime.strptime(tweet_time, '%Y-%m-%d %H:%M:%S%z')

    int(mention_count)
    float(price_at_tweet)

    sql = """
    insert into twitter_crypto_mentions
    values (%s,%s,%s,%s,%s);
    """
    cursor.execute(sql, (tweet_time, user, coin, mention_count, price_at_tweet))
    
    print(f"Tweet data about {coin} was inserted into the database")
    db.commit()

