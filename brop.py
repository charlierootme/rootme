from pwn import *
import random

chal_url = "challenge03.root-me.org"
chal_port= 56543

def input_generator(size):
	def input_gen():
		return "A"*size
	return input_gen
	
def player_input_generator():
	return random.choice("rock/paper/scissors".split("/"))

def play(input_gen_func = player_input_generator, display = False):
	r = remote(chal_url, chal_port)
	ret_progress=0
	try:
		while True:
			rl = r.readuntil(":")
			if display:
				print rl
			r.send(input_gen_func())
			rl = r.readline()
			if display:
				print rl
			ret_progress+=1
			rl = r.readline()
			if display:
				print rl		
			ret_progress+=1
	except:
		pass
	r.close()
	return ret_progress
	
count = play(display=True)
new_count = count
size = 5
print 'count =',count,'size = ',size
while count == new_count:
	new_count = play(display=False, input_gen_func = input_generator(size))
	size +=1
count = new_count
print 'count =',count,'size = ',size

while count == new_count:
	new_count = play(display=False, input_gen_func = input_generator(size))
	size +=1
count = new_count
print 'count =',count,'size = ',size
