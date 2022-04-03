# Twitter-Crypto-Mention-Capture
Using Python Tweepy and Apache Kafka. Data is streamed from Twitter's API containing selected crypto currencies and their price from Coingecko's API and stores results in a MySQL database. 

- Program was created in a linux environment on Windows Subsystem for Linux. 
- Apache Kafka needs to be installed for this program to work
- A Twitter developer account is needed to run the Twitter API
- Coingecko's API should be used to select different currencies to track.  https://www.coingecko.com/en/api/documentation?
- You will need to create a topic named 'crypto' in Kafka or alter the code accordingly.
- Data captured is tweet time, username, price at tweet, and count of mentions. Allows analyses to be conducted based on price movement and social activity for select currencies.
- The database.py file will need to be updated with the user's MySQL login information.
