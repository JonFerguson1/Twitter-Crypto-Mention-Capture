import requests
import tweepy
from kafka import KafkaProducer

# Enter your Twitter API Keys here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

producer = KafkaProducer(bootstrap_servers='localhost:9092')

TOPIC = 'crypto'

# Functions for grabbing the updated price 

def get_VRA_price():
    vra_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=verasity&vs_currencies=usd", 
                   headers = {"accept": "application/json"})
    vra = vra_req.json()['verasity']['usd']

    return vra

def get_MOVR_price():
    movr_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=moonriver&vs_currencies=usd",
                   headers = {"accept": "application/json"})
    movr = movr_req.json()['moonriver']['usd']

    return movr

def get_VET_price():
    vet_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=vechain&vs_currencies=usd",
                   headers = {"accept": "application/json"})
    vet = vet_req.json()['vechain']['usd']

    return vet

def get_NAKA_price():
    naka_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=nakamoto-games&vs_currencies=usd",
                   headers = {"accept": "application/json"})
    naka = naka_req.json()['nakamoto-games']['usd']

    return naka

def get_GRT_price():
    grt_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=the-graph&vs_currencies=USD",
                   headers = {"accept": "application/json"})
    grt = grt_req.json()['the-graph']['usd']

    return grt

def get_UOS_price():
    uos_req = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=Ultra&vs_currencies=USD",
                   headers = {"accept": "application/json"})
    uos = uos_req.json()['ultra']['usd']

    return uos

#stream by keywords
keywords = ['$VRA', '$MOVR', '$VET', '$NAKA', '$GRT', '$UOS']

# starting mention counts
vra_count = 0
movr_count = 0
vet_count = 0
naka_count = 0
grt_count = 0
uos_count = 0

# runs the Twitter stream once called
class IDPrinter(tweepy.Stream):

    def on_status(self, status):

        if "$VRA" in status.text:
            global vra_count
            coin = "Veracity - VRA"
            vra_count+=1
            mention_count = vra_count
            price_at_tweet = get_VRA_price()
        elif "$MOVR" in status.text:
            global movr_count
            coin = "Moonriver - MOVR"
            movr_count+=1
            mention_count = movr_count
            price_at_tweet = get_MOVR_price()
        elif "$VET" in status.text:
            global vet_count
            coin = "VeChain - VET"
            vet_count+=1
            mention_count = vet_count
            price_at_tweet = get_VET_price()
        elif "$NAKA" in status.text:
            global naka_count
            coin = "Nakamoto Games - NAKA"
            naka_count+=1
            mention_count = naka_count
            price_at_tweet = get_NAKA_price()
        elif "$GRT" in status.text:
            global grt_count
            coin = "The Graph - GRT"
            grt_count+=1
            mention_count = grt_count
            price_at_tweet = get_GRT_price()
        else:
            global uos_count
            uos_count+=1
            coin = "Ultra - UOS"
            mention_count = uos_count
            price_at_tweet = get_UOS_price()

        tweet_time = status.created_at
        user = status.user.screen_name

        message = f"{tweet_time},{user},{coin},{mention_count},{price_at_tweet}"
        message = bytearray(message.encode("utf-8"))
        print("{} | {} | {} | {} | {}".format(tweet_time, user, coin, mention_count, price_at_tweet))
        producer.send(TOPIC, message) # Sends to Kafka topic crypto

# starts the stream
stream_tweet = IDPrinter(consumer_key, consumer_secret, access_token, access_token_secret)
stream_tweet.filter(track=keywords)
