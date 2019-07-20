import sqlite3
from tabulate import tabulate

def setupDB():
	setupLeague()
	setupTeams()
	setupPlayers()
	setupFixtures()
	setupInactivity()
	setupScoreSubmit()
	setupPlayerInvites()

def setupLeague():
    db = sqlite3.connect(r'./mydb.db')
    cursor = db.cursor()
    try:
        cursor.execute('''CREATE TABLE Leagues (
    	ID INTEGER PRIMARY KEY,
    	League_Name TEXT NOT NULL,
    	Chat INTEGER NOT NULL,
    	Scores INTEGER NOT NULL,
        Fixtures INTEGER NOT NULL,
        Team INTEGER NOT NULL,
        Role INTEGER NOT NULL,
		Console TEXT NOT NULL
        );''')
        db.commit()
        db.close
        print("created League Database")
        pass
    except:
        db.close
        print("League Database exists")
        print("Forced Connection close")

def setupTeams():
    db = sqlite3.connect(r'./mydb.db')
    cursor = db.cursor()
    #try:
    cursor.execute('''CREATE TABLE Teams (
	ID INTEGER PRIMARY KEY,
	League_ID INTEGER NOT NULL,
	Team_1 TEXT NOT NULL,
	Team_2 TEXT NOT NULL,
    Team_3 TEXT NOT NULL,
    Team_4 TEXT NOT NULL,
    Team_5 TEXT NOT NULL,
	Manager_1 INTEGER NOT NULL,
	Manager_2 INTEGER NOT NULL,
	Manager_3 INTEGER NOT NULL,
	Manager_4 INTEGER NOT NULL,
	Manager_5 INTEGER NOT NULL
    );''')
    db.commit()
    db.close
    print("created Team Database")
    #    pass
    #except:
    #    db.close
    #    print("Team Database exists")
    #    print("Forced Connection close")

def setupPlayers():
    db = sqlite3.connect(r'./mydb.db')
    cursor = db.cursor()
    try:
        cursor.execute('''CREATE TABLE Players (
    	ID INTEGER PRIMARY KEY,
    	Discord_ID INTEGER NOT NULL,
    	League_ID INTEGER NOT NULL,
    	Team_ID INTEGER NOT NULL
        );''')
        db.commit()
        db.close
        print("created Player Database")
        pass
    except:
        db.close
        print("Team Player exists")
        print("Forced Connection close")

def setupFixtures():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''CREATE TABLE Fixtures (
		ID INTEGER PRIMARY KEY,
		League_ID INTEGER NOT NULL,
		Fixture_Pos INTEGER NOT NULL,
		Team_1 INTEGER NOT NULL,
		Team_2 INTEGER NOT NULL,
		Score_1 INTEGER,
		Score_2 INTEGER,
		Due_Date TEXT NOT NULL
		);''')
		db.commit()
		db.close
		print("created Fixtures Database")
		pass
	except:
		db.close
		print("Fixtures Database exists")
		print("Forced Connection close")

def setupInactivity():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''CREATE TABLE Inactivity (
		ID INTEGER PRIMARY KEY,
		League_ID INTEGER NOT NULL,
		Last_Message INTEGER NOT NULL,
		Last_Online INTEGER NOT NULL
		);''')
		db.commit()
		db.close
		print("created Inactivity Database")
		pass
	except:
		db.close
		print("Team Inactivity exists")
		print("Forced Connection close")

def setupScoreSubmit():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''CREATE TABLE ScoreSubmit (
		ID INTEGER PRIMARY KEY,
		League_ID INTEGER NOT NULL,
		Fixture_Pos INTEGER NOT NULL,
		Team_1 INTEGER NOT NULL,
		Team_2 INTEGER NOT NULL,
		Score_1 INTEGER NOT NULL,
		Score_2 INTEGER NOT NULL,
		Confirmed TEXT
		);''')
		db.commit()
		db.close
		print("created Inactivity Database")
		pass
	except:
		db.close
		print("Team Inactivity exists")
		print("Forced Connection close")

def setupPlayerInvites():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''CREATE TABLE PlayerInvites (
		ID INTEGER PRIMARY KEY,
		League_ID INTEGER NOT NULL,
		Team_ID INTEGER NOT NULL,
		Discord_ID INTEGER NOT NULL
		);''')
		db.commit()
		db.close
		print("created Inactivity Database")
		pass
	except:
		db.close
		print("Team Inactivity exists")
		print("Forced Connection close")

##-setup end-##

#League Functions
def createLeague(LeagueName, LeagueChat,LeagueScores,LeagueFixtures,LeagueTeam,LeagueRole,Console):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO Leagues(League_Name,Chat,Scores,Fixtures,Team,Role,Console)
		VALUES(?,?,?,?,?,?,?)''', (LeagueName,LeagueChat,LeagueScores,LeagueFixtures,LeagueTeam,LeagueRole,Console,))
		db.commit()
		db.close()
		print("Created league")
	except:
		db.close
		print("Forced Connection close")

def deleteLeague(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM Leagues WHERE ID = ?''',(ID,))
		db.commit()
		db.close()
		print("Deleted League Success")
	except:
		db.close()
		print("Failed to delete league")
		print("Forced Connection close")

def getLeagueID(objectID,type):
	if type == "League_Name" or type == "Chat" or type == "Scores" or type == "Fixtures" or type == "Team" or type == "Role":
		db = sqlite3.connect(r'./mydb.db')
		cursor = db.cursor()
		cursor.execute("SELECT ID FROM Leagues WHERE " + type + "=?", (objectID,))
		try:
			data=cursor.fetchone()
			ID = data[0]
			db.close()
			return ID
			pass
		except:
			print("Failed to get League Object ID")
			db.close()
			return 0
	else:
		print("Error database type does not exist")

def getLeagueObjectID(ID,object):
	if object == "League_Name" or object == "Chat" or object == "Scores" or object == "Fixtures" or object == "Team" or object == "Role":
		db = sqlite3.connect(r'./mydb.db')
		cursor = db.cursor()
		cursor.execute("SELECT " + object + " FROM Leagues WHERE ID=?", (ID,))
		try:
			data=cursor.fetchone()
			objectID = data[0]
			db.close()
			return objectID
			pass
		except:
			print("Failed to get League ID")
			db.close()
			return 0
	else:
		print("Error database type does not exist")

def getLastLeagueID():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT rowid from Leagues order by ROWID DESC limit 1")
	try:
		data=cursor.fetchone()
		objectID = data[0]
		db.close()
		return objectID
		pass
	except:
		print("Counted zero leagues")
		db.close()
		return 0

def countLeagues():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT count(*) from Leagues")
	try:
		data=cursor.fetchone()
		objectID = data[0]
		db.close()
		return objectID
		pass
	except:
		print("Counted zero leagues")
		db.close()
		return 0

def updateManager(League_ID,Team_ID,Manager):
	db = sqlite3.connect(r'./mydb.db')
	try:
		cursor = db.cursor()
		cursor.execute("UPDATE Teams SET Manager_"+str(Team_ID)+"=? WHERE League_ID=?", (Manager,League_ID,))
		db.commit()
		db.close()
		pass
	except:
		print("Failed")
		db.close()

def getManager(League_ID,Team_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT Manager_" + str(Team_ID) + " FROM Teams WHERE League_ID=?", (League_ID,))
	try:
		data=cursor.fetchone()
		objectID = data[0]
		db.close()
		return objectID
		pass
	except:
		print("Failed to get manager")
		db.close()
		return 0
#Teams
def createLeagueTeams(League_ID,Manager_1,Manager_2,Manager_3,Manager_4,Manager_5):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO Teams(League_ID,Team_1,Team_2,Team_3,Team_4,Team_5,Manager_1,Manager_2,Manager_3,Manager_4,Manager_5)
		VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (League_ID,"Team 1","Team 2","Team 3","Team 4","Team 5",Manager_1,Manager_2,Manager_3,Manager_4,Manager_5,))
		db.commit()
		db.close()
		print("Created Team")
	except:
		db.close
		print("Forced Connection close")

def deleteLeagueTeams(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM Teams WHERE League_ID = ?''',(League_ID,))
		db.commit()
		db.close()
		print("Deleted League Success")
	except:
		db.close()
		print("Failed to delete league")
		print("Forced Connection close")

#Players
def createPlayeronTeam(Discord_ID,League_ID,Team_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO Players(Discord_ID,League_ID,Team_ID)
		VALUES(?,?,?)''', (Discord_ID,League_ID,Team_ID,))
		db.commit()
		db.close()
		print("Created Player")
	except:
		db.close
		print("Forced Connection close")

def deleteAllPlayers(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM Players WHERE League_ID = ?''',(League_ID,))
		db.commit()
		db.close()
		print("Deleted Team Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def deletePlayer(Discord_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM Players WHERE Discord_ID = ?''',(Discord_ID,))
		db.commit()
		db.close()
		print("Deleted Player Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def getTeamNumber(Discord_ID):
		db = sqlite3.connect(r'./mydb.db')
		cursor = db.cursor()
		cursor.execute("SELECT Team_ID FROM Players WHERE Discord_ID=?", (Discord_ID,))
		try:
			data=cursor.fetchone()
			ID = data[0]
			db.close()
			return ID
			pass
		except:
			print("Failed to get League Object ID")
			db.close()
			return 0

def getLeagueNumber(Discord_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT League_ID FROM Players WHERE Discord_ID=?", (Discord_ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get League Object ID")
		db.close()
		return 0

def getLeagueName(Discord_ID):
	ID = getLeagueNumber(Discord_ID)
	LeagueName = getLeagueObjectID(ID,"League_Name")
	return LeagueName

def getTeamName(Discord_ID):
	League_ID = getLeagueNumber(Discord_ID)
	Team_ID = getTeamNumber(Discord_ID)
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT Team_" + str(Team_ID) +" FROM Teams WHERE League_ID=?", (League_ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get team name")
		db.close()
		return 0

def getTeamNameID(League_ID,Team_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT Team_" + str(Team_ID) +" FROM Teams WHERE League_ID=?", (League_ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get team name")
		db.close()
		return 0

def changeTeamName(Discord_ID, Team_Name):
	League_ID = getLeagueNumber(Discord_ID)
	Team_ID = getTeamNumber(Discord_ID)
	db = sqlite3.connect(r'./mydb.db')
	try:
		cursor = db.cursor()
		cursor.execute("UPDATE Teams SET Team_"+str(Team_ID)+"=? WHERE League_ID=?", (Team_Name,League_ID,))
		db.commit()
		db.close()
		pass
	except:
		print("Failed")
		db.close()

def getTeams(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT * FROM Teams WHERE League_ID=?", (League_ID,))
	data = cursor.fetchall()
	db.close()
	return data

def getTeamNames(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT * FROM Teams WHERE League_ID=?", (League_ID,))
	data = cursor.fetchall()
	db.close()
	return data

def getTeamMembers(League_ID, Team_Name):
	TeamID = getTeamIDByName(League_ID,Team_Name)
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT Discord_ID FROM Players WHERE League_ID=? and Team_ID=?", (League_ID,TeamID,))
	data = cursor.fetchall()
	db.close()
	return data

def getTeamIDByName(League_ID, TeamName):
	Team_names = getTeamNames(League_ID)
	if(TeamName == Team_names[0][2]):
		return 1
	elif(TeamName == Team_names[0][3]):
		return 2
	elif(TeamName == Team_names[0][4]):
		return 3
	elif(TeamName == Team_names[0][5]):
		return 4
	elif(TeamName == Team_names[0][6]):
		return 5
	else:
		return 0

#Fixtures
def addFixture(League_ID, Fixture_Pos, Team_1, Team_2,Due_Date):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO Fixtures(League_ID,Fixture_Pos,Team_1,Team_2,Due_Date)
		VALUES(?,?,?,?,?)''', (League_ID,Fixture_Pos,Team_1,Team_2,Due_Date,))
		db.commit()
		db.close()
		print("Created Fixture")
	except:
		db.close()
		print("Forced Connection close")

def checkFixtureDueDate():
	dog="cat"
	return dog

def addFixtureScore(League_ID,Fixture_Pos,Score_1,Score_2):
	db = sqlite3.connect(r'./mydb.db')
	try:
		cursor = db.cursor()
		cursor.execute("UPDATE Fixtures SET Score_1=?, Score_2=? WHERE League_ID=? and Fixture_Pos=?", (Score_1,Score_2,League_ID,Fixture_Pos,))
		db.commit()
		db.close()
		pass
	except:
		print("Failed")
		db.close()

def getFixture(League_ID,Fixture_ID):
	fixtures = []
	FixtureNth = (Fixture_ID*2)-2
	data = getAllFixtures(League_ID)
	try:
		fixtures.append(data[FixtureNth])
		pass
	except:
		print("Fixture Missing")
	try:
		fixtures.append(data[FixtureNth+1])
		pass
	except:
		print("Fixture Missing")
	return fixtures

def getMatch(League_ID,MatchID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT * FROM Fixtures WHERE League_ID=? and Fixture_Pos=?", (League_ID,MatchID,))
	data = cursor.fetchall()
	db.close()
	return data

def getAllFixtures(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT * FROM Fixtures WHERE League_ID=?", (League_ID,))
	data = cursor.fetchall()
	db.close()
	return data

def deleteLeagueFixtures(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM Fixtures WHERE League_ID = ?''',(League_ID,))
		db.commit()
		db.close()
		print("Deleted Fixtures Success")
	except:
		db.close()
		print("Failed to delete Fixtures")
		print("Forced Connection close")

#invite
def invitePlayer(League_ID,Team_ID,Discord_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO PlayerInvites(League_ID,Team_ID,Discord_ID)
		VALUES(?,?,?)''', (League_ID,Team_ID,Discord_ID,))
		db.commit()
		db.close()
		print("Added Player Invite")
	except:
		db.close()
		print("Forced Connection close")

def deleteInvitePlayer(Discord_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM PlayerInvites WHERE Discord_ID = ?''',(Discord_ID,))
		db.commit()
		db.close()
		print("Deleted Invite Success")
	except:
		db.close()
		print("Failed to delete Invite")
		print("Forced Connection close")

def deleteInvite(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM PlayerInvites WHERE ID = ?''',(ID,))
		db.commit()
		db.close()
		print("Deleted Invite Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def deleteInvitesLeague(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM PlayerInvites WHERE League_ID = ?''',(League_ID,))
		db.commit()
		db.close()
		print("Deleted Invite Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def getInviteTeam(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT Team_ID FROM PlayerInvites WHERE ID=?", (ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get invite Team")
		db.close()
		return 0

def getInviteUser(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT Discord_ID FROM PlayerInvites WHERE ID=?", (ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get invite Team")
		db.close()
		return 0

def getInviteLeague(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT League_ID FROM PlayerInvites WHERE ID=?", (ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get invite League")
		db.close()
		return 0

def getInviteID(League_ID,Team_ID,Discord_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT ID FROM PlayerInvites WHERE League_ID=? and Team_ID=? and Discord_ID=? ", (League_ID,Team_ID,Discord_ID,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get invite League")
		db.close()
		return 0

#ScoreSubmit
def submitScore(League_ID,Fixture_Pos,Score_1,Score_2):
	match = getMatch(League_ID,Fixture_Pos)[0]
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO ScoreSubmit(League_ID,Fixture_Pos,Team_1,Team_2,Score_1,Score_2)
		VALUES(?,?,?,?,?,?)''', (League_ID,Fixture_Pos,match[3],match[4],Score_1,Score_2,))
		db.commit()
		db.close()
		print("Added Score Submit")
	except:
		db.close()
		print("Forced Connection close")

def deleteScore(League_ID,Fixture_Pos):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM ScoreSubmit WHERE League_ID=? and Fixture_Pos=?''',(League_ID,Fixture_Pos,))
		db.commit()
		db.close()
		print("Deleted Invite Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def getScore(ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT * FROM ScoreSubmit WHERE ID=?", (ID,))
	try:
		data=cursor.fetchall()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get score submit")
		db.close()
		return 0

def getScoreSubmitID(League_ID,Fixture_Pos):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	cursor.execute("SELECT ID FROM ScoreSubmit WHERE League_ID=? and Fixture_Pos=?", (League_ID,Fixture_Pos,))
	try:
		data=cursor.fetchone()
		ID = data[0]
		db.close()
		return ID
		pass
	except:
		print("Failed to get score submit")
		db.close()
		return 0

def deleteScoreSubmitLeague(League_ID):
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
	try:
		cursor.execute('''DELETE FROM ScoreSubmit WHERE League_ID=?''',(League_ID,))
		db.commit()
		db.close()
		print("Deleted Invite Success")
	except:
		db.close()
		print("Failed to delete Team")
		print("Forced Connection close")

def calculateTable(League_ID):
	fixtures = getAllFixtures(1)
	#0  |1|2|3|4 |5 |6 |7  |8
	#PLD|W|D|L|SF|SA|SD|PTS|Team
	Table = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
	for match in fixtures:
		#3 points win, 1 point draw
		#Check match played
		if(match[5] is not None):
			Team_1 = match[3]-1
			Team_2 = match[4]-1
			Score_1 = match[5]
			Score_2 = match[6]
			Table[Team_1][0] = Table[Team_1][0]+1
			Table[Team_2][0] = Table[Team_2][0]+1
			#Check draw
			if(Score_1 == Score_2):
				Table[Team_1][2] = Table[Team_1][2]+1
				Table[Team_2][2] = Table[Team_2][2]+1
			elif(Score_1 > Score_2):
				Table[Team_1][1] = Table[Team_1][1]+1
				Table[Team_2][3] = Table[Team_2][3]+1
			elif(Score_1 < Score_2):
				Table[Team_1][3] = Table[Team_1][3]+1
				Table[Team_2][1] = Table[Team_2][1]+1
			#Calculate SF SA
			Team_1_SF = Score_1
			Team_1_SA = Score_2
			Team_2_SF = Score_2
			Team_2_SA = Score_1
			Table[Team_1][4] = Table[Team_1][4] + Team_1_SF
			Table[Team_1][5] = Table[Team_1][5] + Team_1_SA
			Table[Team_2][4] = Table[Team_2][4] + Team_2_SF
			Table[Team_2][5] = Table[Team_2][5] + Team_2_SA
			#Calculate SD
			Table[Team_1][6] = Table[Team_1][4] - Table[Team_1][5]
			Table[Team_2][6] = Table[Team_2][4] - Table[Team_2][5]
			#Calculate Points
			Team_1_Pts = (Table[Team_1][1]*3) + (Table[Team_1][2]*1)
			Team_2_Pts = (Table[Team_2][1]*3) + (Table[Team_2][2]*1)
			Table[Team_1][7] = Team_1_Pts
			Table[Team_2][7] = Team_2_Pts
	sorted_table = sorted(Table, key=lambda x: x[7], reverse=True)
	counter = 0
	for row in Table:
		counter = counter + 1
		row.append(counter)
		#print(row)
	sorted_table = sorted(Table, key=lambda x: x[7], reverse=True)

	counter = 0
	msgtable = [["Pos","Team","PLD","W","D","L","SF","SA","SD","PTS"]]
	for row in sorted_table:
		counter = counter + 1
		msgtable.append([counter,getTeamNameID(League_ID,row[8]),row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]])
		#print(row[7])
	tab = tabulate(msgtable)
	return tab

def getInvites():
	db = sqlite3.connect(r'./mydb.db')
	cursor = db.cursor()
    #get teams in list
	cursor.execute("SELECT * FROM PlayerInvites")
	data = cursor.fetchall()
	db.close()
	tab = tabulate(data)
	return(tab)


#Inactivity
def addUser():
	dog="cat"

def updateLastMessage():
	dog="cat"

def updateLastOnline():
	dog="cat"

def getLastOnline():
	dog="cat"
	return dog

def getLastMessage():
	dog="cat"
	return dog
