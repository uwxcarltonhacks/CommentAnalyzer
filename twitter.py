#Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import API
import json
import re
from watson_developer_cloud import ToneAnalyzerV3
import sys

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='SgwSyRomsfn-o6-hO4OSwfwQDI5SiT_22cBcPjHemOBu',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

#Variables that contains the user credentials to access Twitter API 
access_token = "2237159415-kEiwPGBZJWUsTYhmUdkUiS1hX0GiiwVEhPseC1F"
access_token_secret = "9J5ylgtPuhkSKKh10jGylS8CmSKsFZP5mLJcsbFBlw74k"
consumer_key = "nqXHh0t7oJpGbdeGhp2PGmP81"
consumer_secret = "bXcaZmYR1kqaWXNHLDKBBH6ngNkGkkAA3WhYTXJEaeRo8HMnmP"

tweetString = ""
tweetList = []
tones = {}

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

if (len(sys.argv) > 1):
	search = "#" + sys.argv[1]
else:
	search = "#python"

search_results = api.search(q=search, count=100)
for i in range(len(search_results)):
	tweet = json.loads(json.dumps(search_results[i]._json)).get('text')
	if ('RT @' in tweet):
		tweet = tweet.split(": ", 1)[1]

	tweetList.append(tweet)
	tweetString += tweet

# # for text in tweetList:
tone_analysis = tone_analyzer.tone(
	{'text': tweetString},
	'application/json'
).get_result()

tweetSentences = json.loads(json.dumps(tone_analysis, indent=2)).get("sentences_tone")

for sentence in tweetSentences:
	for tone in sentence.get("tones"):
		tone = tone.get("tone_id")
		tones[tone] = tones.get(tone, 0) + 1

print(tones)
sys.stdout.flush()