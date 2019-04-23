import re
import nltk
import tweepy 
from tweepy import OAuthHandler 
from ibm_watson import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

class TwitterClient(object): 
	''' 
	Generic Twitter Class for analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		# keys and tokens from the Twitter Dev Console 
		consumer_key = ''
		consumer_secret = ''
		access_token = ''
		access_token_secret = ''

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweets(self, query, count): 
		''' 
		Main function to fetch tweets and parse them.
		Returns an array of arrays of tokenized tweets.
		'''
		# empty string to store parsed tweets as a paragraph
		tweets = ""

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet = self.clean_tweet(tweet.text)
				 # '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) 
				# saving sentiment of tweet 
				# parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets = tweets + parsed_tweet + '. '
				else: 
					tweets = tweets + parsed_tweet + '. '

			# return parsed and tokenized tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e))

	def get_sentiment(self, tweets):
		"""
		gets the overall sentiment from all of the tweets
		"""
		tone_analysis = tone_analyzer.tone(
			{'text': tweets},
		    content_type='application/json'
		).get_result()

		doc_tones = tone_analysis['document_tone']['tones']
		final_tones = []
		for tone in doc_tones:
			final_tones.append(tone['tone_name'])

		return final_tones

def main(): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	# tweets = api.get_tweets(query = 'slang', count = 1000) 


if __name__ == "__main__": 
	# calling main function 
	main() 
