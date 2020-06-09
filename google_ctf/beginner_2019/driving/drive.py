
import requests
import math
from bs4 import BeautifulSoup

class movement(object):
	def __init__(self, increment=.0001, op= None, direction = None):
		self.increment = increment
		self.x = increment
		self.y = increment
		self.op = op
		self.direction = direction
		self.params = {
			'lat': 51.6498,
			'lon': 0.0982,
			'token': 'gAAAAABe3UWQWcjCsODZXw56qLaOwi1YjBvTX8A9xtEjjLmtsBnfikq5LYfWQx0RNPaH70uhABhMnT7y1Z7zec5pq7Vlslbrd0JSVkh8I6vkBkpvu1v2alko7cLlj4mcwORKzYGkdqNW'
		}
	def north(self):
		self.params['lon'] += self.y
		# self.params['lon'] = round(self.params['lon'],4)
	def south(self):
		self.params['lon'] -= self.y
		# self.params['lon'] = round(self.params['lon'],4)
	def east(self):
		self.params['lat'] += self.x
		# self.params['lat'] = round(self.params['lat'],6)
	def west(self): 
		self.params['lat'] -= self.x
		# self.params['lat'] = round(self.params['lat'],6)
	def ne(self): 
		self.north()
		self.east()
	def se(self):
		self.south()
		self.east()
	def nw(self):
		self.north()
		self.west()
	def sw(self):
		self.south()
		self.west()
	def rotate(self, degree, direction):
		radians = degree * math.pi / 180
		temp = -1
		if direction == 'x': # rotate in the x direction by 1 degree clockwise
			dy = math.tan(radians) * self.x # tan theta * adjacent = opposite
			self.y -= dy
		else:
			dx = self.y / math.tan(radians)
			self.x -= dx


	def cont(self):
		# print('continuing')
		if self.direction == 'n':
			self.north()
		elif self.direction == 's':
			self.south()
		elif self.direction == 'w':
			self.west()
		elif self.direction == 'e':
			self.east()
		elif self.direction == 'ne':
			self.ne()
		elif self.direction == 'se':
			self.se()
		elif self.direction == 'sw':
			self.sw()
		elif self.direction == 'nw':
			self.nw()
	def rc(self): # rotate clockwise
		if self.direction == 'n':
			self.direction = 'ne'
		elif self.direction == 's':
			self.direction = 'sw'
		elif self.direction == 'w':
			self.direction = 'nw'
		elif self.direction == 'e':
			self.direction = 'se'
		elif self.direction == 'ne':
			self.direction = 'e'
		elif self.direction == 'se':
			self.direction = 's'
		elif self.direction == 'sw':
			self.direction = 'w'
		elif self.direction == 'nw':
			self.direction = 'n'
	def opposite(self): # reverse direction
		if self.direction == 'n':
			self.direction = 's'
		elif self.direction == 's':
			self.direction = 'n'
		elif self.direction == 'w':
			self.direction = 'e'
		elif self.direction == 'e':
			self.direction = 'w'
		elif self.direction == 'ne':
			self.direction = 'sw'
		elif self.direction == 'se':
			self.direction = 'nw'
		elif self.direction == 'sw':
			self.direction = 'ne'
		elif self.direction == 'nw':
			self.direction = 'se'

	def rc_c(self): # rotate counterclockwise
		if self.direction == 'n':
			self.direction = 'nw'
		elif self.direction == 'se':
			self.direction = 'n'
		elif self.direction == 'w':
			self.direction = 'sw'
		elif self.direction == 'e':
			self.direction = 'ne'
		elif self.direction == 'ne':
			self.direction = 'n'
		elif self.direction == 'se':
			self.direction = 'e'
		elif self.direction == 'sw':
			self.direction = 's'
		elif self.direction == 'nw':
			self.direction = 'w'

def main():
	# api-endpoint 
	# url = 'https://drivetothetarget.web.ctfcompetition.com/?lat=' + str(lat) + '&' + str(lon) +\
	# 'lon=' + '&token=gAAAAABe3UN4rqOEQ2ORqbaAXbiMdd571C-HFJ4fK8j8QuDpmZU2EGSDFBjGwT0592QvBlfjfALgRBbRZSdZyGP0n5FNH-XPG1VwNG35bMGb3fQZ4kob3xie4y5IIspuVALKbpRGnF4-'
	
	# setup
	url2 = 'https://drivetothetarget.web.ctfcompetition.com/?'
	agent = movement(increment = .0001, op='p', direction = 's') # p is for plus, m is for minus
	# print(agent.params)	
	agent.cont()
	# print(agent.params)
	while(1):
		r = requests.get(url = url2, params = agent.params)
		soup = BeautifulSoup(r.text, features="html.parser")
		token = soup.find("input", attrs={"name": "token"})["value"] 
		for k in r.iter_lines():
			temp = str(k)
			if 'CTF' in temp:
				print(k)
				break
			elif '<p>' in temp:	
				if 'closer' in temp:
					print(agent.params)
					print('closer')
					agent.cont()
				elif 'getting away' in temp:
					# print(agent.params)
					print('getting away')
					agent.opposite()
					agent.cont()
					agent.opposite()
					agent.rc() # rotate clockwise
					agent.rc()
					# agent.rotate(1, 'x') # rotate 1 degree
					agent.cont() # try again
				elif 'too far' in temp:
					print(agent.params)
					print('too far', temp)
					agent.opposite() # first, reverse the direction
					agent.cont() # move back one
					agent.opposite()
					# agent.rotate(1, 'x')
					agent.rc()  # rotate clockwise
					agent.rc()
					agent.cont() # try again
				else: 
					print(temp)
					continue
		# print(token)
		agent.params['token'] = token 
		# break




	
if __name__ == '__main__':
	main()