def primeFunction(): 
	prime = None
	num = 1
	while True: 
		num = num + 1

		for i in range(2, num): 
			if(num % i) == 0: 
				prime = False
				break
			else: 
				prime = True

		if prime: 
			
			# yields the value to the caller 
			# and halts the execution 
			yield num 

def mainn(): 
	
	# returns the generator object. 
	prime = primeFunction() 
	
	# generator executes upon request 
	for i in prime: 
		print(i) 
		if i > 50: 
			break

if __name__ == "__main__": 
	mainn() 
