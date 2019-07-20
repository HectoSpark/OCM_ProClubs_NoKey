import random
def generateFixture():
	ran = random.randint(0,2)
	f = open("gameorders/gameorder-" + str(ran) + ".txt")
	games = []
	onecount = 0
	twocount = 0
	threecount = 0
	fourcount = 0
	fivecount = 0
	for x in f:
		if x.find('1') > -1:
			onecount = onecount + 1;
		if x.find('2') > -1:
			twocount = twocount + 1;
		if x.find('3') > -1:
			threecount = threecount + 1;
		if x.find('4') > -1:
			fourcount = fourcount + 1;
		if x.find('5') > -1:
			fivecount = fivecount + 1;
		x = x.replace('\n','')
		x = x.split('V')
		games.append([x[0],x[1]])
		#print(x)
	#print(games)
	print('1 = ' + str(onecount))
	print('2 = ' + str(twocount))
	print('3 = ' + str(threecount))
	print('4 = ' + str(fourcount))
	print('5 = ' + str(fivecount))
	f.close()
	return games
