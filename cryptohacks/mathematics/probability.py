import numpy as np
import math
import ast
from time import sleep
import requests

# Brute force to solve Jack's Birthday Hash
def jbh_solve():
	url = 'https://cryptohack.org/api/submit/birthday1.json'
	obj = {'flag':1, '_csrf_token':'9bcxvzj5fha83py2jbj6hdm1ixctee1r68e2hqpktkrc2y6qszikidhzhpz14x1x'}
	c = {'session': 'eyJfY3NyZl90b2tlbiI6IjliY3h2emo1ZmhhODNweTJqYmo2aGRtMWl4Y3RlZTFyNjhlMmhxcGt0a3JjMnk2cXN6aWtpZGh6aHB6MTR4MXgiLCJ1c2VyX2lkIjoxODUwMX0.YIZQaw.BCHNZdI89vYBbO7jLSzUfg3p0IU'}
	r = requests.post(url, data =obj, cookies = c)
	i = 273
	for j in range(2048):
		d = ast.literal_eval(r.text)
		if d["message"] == "You are doing that too fast!":
			print ("Waiting")
			sleep(5)
			i-=1
		elif d["message"] != "Incorrect flag":
			print("Answer is ", i)
			break

		i+=1
		sleep(1)
		obj['flag'] = i
		r = requests.post(url, data=obj, cookies = c)
		print("sending", i, "received", r.text)

def main():
	print(np.log(1-.5) / np.log(1-(1/pow(2,11))))

	n = np.sqrt(2 * pow(2, 11) * -np.log(.25))
	print(n)

if __name__ == '__main__':
	main()