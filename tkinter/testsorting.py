testdict = [
	{"age":3},
	{"age":2},
	{"age":15},
	{"age":10},
	{"age":-1}]
	
for item in sorted(testdict, key = lambda item: item["age"]):
	print(item)