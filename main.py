import discord
import locale
import asyncio
from discord.ext import commands
from discord import Permissions
from discord import User
from datetime import datetime, timedelta
import database as db
import fixture as fx
import random

client = commands.Bot(command_prefix = "!")
#channel ids
setconsole_channel = 591615333790515223
guildid = 591598458939506707

League = ""
Console = ""

LeagueNumber = 0

@client.event
async def on_ready():
	locale.setlocale(locale.LC_ALL,'')
	print("OCM Pro Clubs online")
	print("Started waiting list count")
	await countwaitinglists()


###-Waiting lists-###
##PS4 waiting list
@client.command(pass_context=True)
async def PS4(message):
	if message.channel.id == setconsole_channel:
		member = discord.utils.get(message.guild.members, id = message.author.id)
		role = discord.utils.get(message.guild.roles, name="PS4")
		rolewaiting = discord.utils.get(message.guild.roles, name="Not Queued")
		banterchat = discord.utils.get(message.guild.channels, name="banter-chat")
		Name = str(member.name)
		print(Name + " accepted terms and added accepted-TOC role")
		await member.add_roles(role)
		await member.add_roles(rolewaiting)
		Name = str(member.name)
		await banterchat.send('Welcome to OCM ' + Name + "!")

#Xbox Waiting List
@client.command(pass_context=True)
async def Xbox(message):
	if message.channel.id == setconsole_channel:
		member = discord.utils.get(message.guild.members, id = message.author.id)
		role = discord.utils.get(message.guild.roles, name="Xbox One")
		rolewaiting = discord.utils.get(message.guild.roles, name="Not Queued")
		banterchat = discord.utils.get(message.guild.channels, name="banter-chat")
		Name = str(member.name)
		print(Name + " accepted terms and added accepted-TOC role")
		await member.add_roles(role)
		await member.add_roles(rolewaiting)
		Name = str(member.name)
		await banterchat.send('Welcome to OCM ' + Name + "!")

##-League Creation-##
@client.command(pass_context=False)
@commands.has_role("Directors")
async def move_ps4_waiting(ctx, message:str):
	#role = discord.utils.get(message.guild.roles, name=League)
	global League
	League = message
	await create_League()
	await PS4_waiting_priv_update()

@client.command(pass_context=False)
@commands.has_role("Directors")
async def move_xbox_waiting(ctx, message:str):
	global League
	League = message
	await create_League()
	await Xbox_waiting_priv_update()

async def create_League():
	await create_League_Role()
	await create_League_Channel()


async def create_League_Role():
	guild = client.get_guild(guildid)
	await guild.create_role(name=str(League), hoist=True)

async def create_League_Channel():
	#create category
	guild = client.get_guild(guildid)
	await guild.create_category(League)
	findroleID = discord.utils.get(guild.roles, name="Staff")
	finddirectorID = discord.utils.get(guild.roles, name="Directors")
	findteamID = discord.utils.get(guild.roles, name=League)
	findcategoryID = discord.utils.get(guild.categories, name=League)
	print(findcategoryID)
	perms = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False),
		findroleID: discord.PermissionOverwrite(read_messages=True, manage_roles=False, send_messages=True, read_message_history=True, manage_messages=True, mention_everyone=True),
		findteamID: discord.PermissionOverwrite(read_messages=True, manage_roles=False, send_messages=True, read_message_history=True),
		finddirectorID: discord.PermissionOverwrite(read_messages=True, manage_roles=False, send_messages=True, read_message_history=True, manage_messages=True, mention_everyone=True)
	}
	LeagueChat = await guild.create_text_channel("League Chat", overwrites=perms, category = findcategoryID)
	Scores = await guild.create_text_channel("Scores", overwrites=perms, category = findcategoryID)
	Fixtures = await guild.create_text_channel("Fixtures", overwrites=perms, category = findcategoryID)
	Team = await guild.create_text_channel("Team", overwrites=perms, category = findcategoryID)
	#create league on database
	db.createLeague(League,LeagueChat.id,Scores.id,Fixtures.id,Team.id,findteamID.id,Console)
	#print(str(test1.id))

##-multi-channel help function-#
@client.command(pass_context=True)
async def helpme(message):
	print("Help")
    #ID's
	PS4channel = discord.utils.get(message.guild.channels, name="ps4-manager-waiting-room")
	Xboxchannel = discord.utils.get(message.guild.channels, name="xbox-one-manager-waiting-room")
    #if PS4 waiting room
	if(message.channel.id == PS4channel.id):
		print("PS4")
		count = PS4_waiting_count()
		await message.channel.send("We are currently waiting for 15 players to start a league, there are " + str(count) + " out of 15.")
    #if Xbox waiting room
	if(message.channel.id == Xboxchannel.id):
		print("Xbox")
		count = Xbox_waiting_count()
		await message.channel.send("We are currently waiting for 15 players to start a league, there are " + str(count) + " out of 15.")
	#if league chat
	if(message.channel.name == "league-chat"):
		await message.channel.send("This is the chat for your League")
	#if scores chat
	if(message.channel.name == "scores"):
		await message.channel.send("Please submit photos of your scores here")
	#if fixtures chat
	if(message.channel.name == "fixtures"):
		await message.channel.send("New fixtures will appear here after every game")
	#if team chat
	if(message.channel.name == "team"):
		await message.channel.send("This is where teams are displayed")

##-waiting rooms functions-##
#PS4 Waiting room count
def PS4_waiting_count():
    guild = client.get_guild(guildid)
    PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
    count = 0
    for member in guild.members:
        for role in member.roles:
            if role.id == PS4wtRole.id:
                count = count + 1
    return count

#Xbox Waiting room count
def Xbox_waiting_count():
    guild = client.get_guild(guildid)
    XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
    count = 0
    for member in guild.members:
        for role in member.roles:
            if role.id == XboxwtRole.id:
                count = count + 1
    return count

#Update PS4 waiting list privilages
async def PS4_waiting_priv_update():
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueID(League,"League_Name")
	PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
	leaguerole = discord.utils.get(guild.roles, name=League)
	managerrole = discord.utils.get(guild.roles, name="Manager")
	count = 0
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	managers = []
	for member in guild.members:
		for role in member.roles:
			if role.id == PS4wtRole.id:
				count = count + 1
				if count<=5:
					managers.append(member.id)
					await member.add_roles(leaguerole)
					await member.add_roles(managerrole)
					await member.remove_roles(PS4wtRole)
				else:
					await member.remove_roles(PS4wtRole)
					await member.add_roles(rolewaiting)
	db.createLeagueTeams(League_ID,managers[0],managers[1],managers[2],managers[3],managers[4])
	db.createPlayeronTeam(managers[0],League_ID,1)
	db.createPlayeronTeam(managers[1],League_ID,2)
	db.createPlayeronTeam(managers[2],League_ID,3)
	db.createPlayeronTeam(managers[3],League_ID,4)
	db.createPlayeronTeam(managers[4],League_ID,5)

async def Xbox_waiting_priv_update():
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueID(League,"League_Name")
	XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
	leaguerole = discord.utils.get(guild.roles, name=League)
	managerrole = discord.utils.get(guild.roles, name="Manager")
	count = 0
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	managers = []
	for member in guild.members:
		for role in member.roles:
			if role.id == XboxwtRole.id:
				count = count + 1
				if count<=5:
					managers.append(member.id)
					await member.add_roles(leaguerole)
					await member.add_roles(managerrole)
					await member.remove_roles(XboxwtRole)
				else:
					await member.remove_roles(XboxwtRole)
					await member.add_roles(rolewaiting)
	db.createLeagueTeams(League_ID,managers[0],managers[1],managers[2],managers[3],managers[4])
	db.createPlayeronTeam(managers[0],League_ID,1)
	db.createPlayeronTeam(managers[1],League_ID,2)
	db.createPlayeronTeam(managers[2],League_ID,3)
	db.createPlayeronTeam(managers[3],League_ID,4)
	db.createPlayeronTeam(managers[4],League_ID,5)

async def createFixtures():
	fixturedata = fx.generateFixture()
	League_ID = db.getLeagueID(League,"League_Name")
	counter = 0
	lastcount = 0
	delta = 7
	for match in fixturedata:
		if(counter == lastcount + 4):
			delta = delta + 7
			lastcount = counter
		counter = counter + 1
		matchdue = datetime.now() + timedelta(days=delta)
		print(matchdue)
		db.addFixture(League_ID,counter,match[0],match[1],str(matchdue))


#Delete League
@client.command(pass_context=True)
@commands.has_role("Directors")
async def delete_League(ctx, message:str):
	guild = client.get_guild(guildid)
	Category = discord.utils.get(guild.channels, name=message)
	leaguerole = discord.utils.get(guild.roles, name=message)
	XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
	PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
	XboxRole = discord.utils.get(guild.roles, name="Xbox One")
	PS4Role = discord.utils.get(guild.roles, name="PS4")
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	managerrole = discord.utils.get(guild.roles, name="Manager")

	for member in guild.members:
		PS4 = False
		Xbox = False
		Leaguebool = False
		for role in member.roles:
			if role.id == leaguerole.id:
				Leaguebool = True
			if role.id == PS4Role.id:
				PS4 = True
			if role.id == XboxRole.id:
				Xbox = True
		if(Leaguebool == True):
			await member.remove_roles(leaguerole)
			await member.remove_roles(managerrole)
			if(PS4 == True):
				print("PS4")
				await member.add_roles(rolewaiting)
			if(Xbox == True):
				print("Xbox")
				await member.add_roles(rolewaiting)



	for channel in Category.channels:
		await channel.delete()
	await Category.delete()
	await leaguerole.delete()
	leagueID = db.getLeagueID(message,"League_Name")
	print("League ID:" + str(leagueID))
	db.deleteLeague(leagueID)
	db.deleteLeagueTeams(leagueID)
	db.deleteAllPlayers(leagueID)
	db.deleteInvitesLeague(leagueID)
	db.deleteLeagueFixtures(leagueID)
	db.deleteScoreSubmitLeague(leagueID)
	#DATABASE DELETE HERE
	#print(Category.id)

#Join waiting room
@client.command(pass_context=True)
async def join(ctx):
	guild = client.get_guild(guildid)
	XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
	PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
	XboxRole = discord.utils.get(guild.roles, name="Xbox One")
	PS4Role = discord.utils.get(guild.roles, name="PS4")
	member = discord.utils.get(ctx.guild.members, id = ctx.author.id)
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	PS4Waiting = discord.utils.get(guild.channels, name="ps4-manager-waiting-room")
	XboxWaiting = discord.utils.get(guild.channels, name="xbox-one-manager-waiting-room")
	for role in member.roles:
		if role.id == XboxRole.id:
			await member.add_roles(XboxwtRole)
			count = Xbox_waiting_count()
			await XboxWaiting.send(ctx.author.name +" has joined the waiting list")
			await XboxWaiting.send("We are currently waiting for 5 managers to start a league, there are " + str(count) + " out of 15.")
		if role.id == PS4Role.id:
			await member.add_roles(PS4wtRole)
			count = PS4_waiting_count()
			await PS4Waiting.send(ctx.author.name +" has joined the waiting list")
			await PS4Waiting.send("We are currently waiting for 5 managers to start a league, there are " + str(count) + " out of 15.")
	await member.remove_roles(rolewaiting)
	await ctx.message.delete()
	#add to announce member arriving in waiting room

async def countwaitinglists():
	global LeagueNumber
	global League
	global Console
	while True:
		PS4Count = PS4_waiting_count()
		XboxCount = Xbox_waiting_count()
		if PS4Count >= 5:
			Console = "PS4"
			LeagueNumber = db.getLastLeagueID()
			LeagueNumber = LeagueNumber + 1
			League = "League-" + str(LeagueNumber)
			await create_League()
			await PS4_waiting_priv_update()
			await createFixtures()
		if XboxCount >= 5:
			Console = "Xbox"
			LeagueNumber = LeagueNumber + 1
			League = "League-" + str(LeagueNumber)
			await create_League()
			await Xbox_waiting_priv_update()
			await createFixtures()
		await asyncio.sleep(30)

@client.command(pass_context=True)
async def leaveWaitingRoom(ctx):
	guild = client.get_guild(guildid)
	XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
	PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	member = discord.utils.get(ctx.guild.members, id = ctx.author.id)
	await member.add_roles(rolewaiting)
	await member.remove_roles(XboxwtRole)
	await member.remove_roles(PS4wtRole)

#invites
@client.command(pass_context=True)
@commands.has_role("Manager")
async def invite(ctx, user:User):
	guild = client.get_guild(guildid)
	player = user.mention.replace("<@","").replace(">","")
	invitee = discord.utils.get(guild.members, id = int(player))
	teamID = db.getTeamNumber(ctx.author.id)
	leagueID = db.getLeagueNumber(ctx.author.id)
	xbox_free_agent = discord.utils.get(guild.channels, name="free-agents-xbox")
	ps4_free_agent = discord.utils.get(guild.channels, name="free-agents-ps4")
	if(ctx.channel.id == xbox_free_agent.id or ctx.channel.id == ps4_free_agent.id):
		if(db.getInviteID(leagueID,teamID,invitee.id) == 0 and db.getLeagueNumber(invitee.id) == 0):
			print(invitee)
			print(invitee.id)
			#create Invite and get team name and ID
			teamname = db.getTeamName(ctx.author.id)

			db.invitePlayer(leagueID,teamID,invitee.id)
			inviteID = db.getInviteID(leagueID,teamID,invitee.id)
			try:
				channel1 = await ctx.author.create_dm()
				await channel1.send("You have invited " + invitee.name + " to join your team " + teamname)
			except:
				await ctx.channel.send("Check your DM settings, something went wrong so we will post this here. \n" + "<@" + str(ctx.author.id) + ">" + "You have invited " + invitee.name + " to join your team " + teamname)
			try:
				channel2 = await invitee.create_dm()
				await channel2.send("You have been invited to join team " + teamname + " by " + ctx.author.name + "\n Type the following to accept: \n !accept " + str(inviteID) + "\n or type the following to decline: \n !decline " + str(inviteID))
			except:
				await ctx.channel.send("Check your DM settings, something went wrong so we will post this here. \n" + "<@" + str(ctx.author.id) + ">" "You have been invited to join team " + teamname + " by " + ctx.author.name + "\n Type the following to accept: \n !accept " + str(inviteID) + "\n or type the following to decline: \n !decline " + str(inviteID))
		else:
			await ctx.channel.send("This player has already been invited or are already in a League!")
	else:
		await ctx.channel.send("This command can only be used in the free agents channels")

@client.command(pass_context=True)
async def accept(ctx,message:str):
	guild = client.get_guild(guildid)
	XboxwtRole = discord.utils.get(guild.roles, name="Xbox One Waiting")
	PS4wtRole = discord.utils.get(guild.roles, name="PS4 Waiting")
	XboxRole = discord.utils.get(guild.roles, name="Xbox One")
	PS4Role = discord.utils.get(guild.roles, name="PS4")
	member = discord.utils.get(guild.members, id = ctx.author.id)
	rolewaiting = discord.utils.get(guild.roles, name="Not Queued")
	PS4Waiting = discord.utils.get(guild.channels, name="ps4-manager-waiting-room")
	XboxWaiting = discord.utils.get(guild.channels, name="xbox-one-manager-waiting-room")

	if(ctx.author.id == db.getInviteUser(message)):
		await ctx.channel.send("We will let the manager know and add you to the League, hang tight!")
		teamID = db.getInviteTeam(message)
		leagueID = db.getInviteLeague(message)
		leagueRole = discord.utils.get(guild.roles, id=db.getLeagueObjectID(leagueID,"Role"))
		leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(leagueID,"Chat"))
		db.deleteInvite(message)
		db.createPlayeronTeam(ctx.author.id,leagueID,teamID)
		await member.add_roles(leagueRole)
		try:
			await member.remove_roles(rolewaiting)
			pass
		except:
			print("Failed to remove queue role")
		try:
			await member.remove_roles(XboxwtRole)
			pass
		except:
			print("Failed to remove xbox role")
		try:
			await member.remove_roles(PS4wtRole)
			pass
		except:
			print("Failed to remove ps4 role")
		teamname = teamname = db.getTeamName(ctx.author.id)
		db.deleteInvitePlayer(ctx.author.id)
		await leagueChat.send("Welcome <@" + str(member.id) + "> to the League, they are joining " + teamname + "!")
	else:
		await ctx.channel.send("This is not a valid invite")

@client.command(pass_context=True)
async def decline(ctx,message:str):
	if(ctx.author.id == db.getInviteUser(message)):
		await ctx.channel.send("Not a problem, we will ignore this invite and delete it!")
		db.deleteInvite(message)
	else:
		await ctx.channel.send("This is not a valid invite")

##Manager Management commands
@client.command(pass_context=True)
@commands.has_role("Manager")
async def changeTeamName(ctx, *, message:str):
	db.changeTeamName(ctx.author.id, message)
	await ctx.channel.send("<@"+str(ctx.author.id)+"> your team name has been changed to " + message)

@client.command(pass_context=True)
async def teams(ctx):
	League_ID = db.getLeagueNumber(ctx.author.id)
	TeamChat_ID = db.getLeagueObjectID(League_ID, "Team")
	if(ctx.channel.id == TeamChat_ID):
		Teams = db.getTeamNames(League_ID)
		print(Teams[0][0])
		print(Teams)
		message = "These are the teams of the League:\n"
		message = message + Teams[0][2] + " - Managed by <@" + str(Teams[0][7]) + ">\n"
		message = message + Teams[0][3] + " - Managed by <@" + str(Teams[0][8]) + ">\n"
		message = message + Teams[0][4] + " - Managed by <@" + str(Teams[0][9]) + ">\n"
		message = message + Teams[0][5] + " - Managed by <@" + str(Teams[0][10]) + ">\n"
		message = message + Teams[0][6] + " - Managed by <@" + str(Teams[0][11]) + ">\n"
		await ctx.channel.send(message)
	else:
		await ctx.channel.send("This command must be run in the Team chat of your League")

@client.command(pass_context=True)
async def squad(ctx, *, message:str):
	League_ID = db.getLeagueNumber(ctx.author.id)
	TeamChat_ID = db.getLeagueObjectID(League_ID, "Team")
	if(ctx.channel.id == TeamChat_ID):
		team = db.getTeamMembers(League_ID, message)
		cmessage = "Here are the squad members of " + message + ":\n"
		for player in team:
			newplayer = str(player)
			newplayer = newplayer.replace("(","").replace(")","").replace(",","")
			cmessage = cmessage + "<@" + str(newplayer) + ">\n"
		await ctx.channel.send(cmessage)
	else:
		await ctx.channel.send("This command must be run in the Team chat of your League")

@client.command(pass_context=True)
async def fixture(ctx, fixturenumber:int):
	League_ID = db.getLeagueNumber(ctx.author.id)
	FixtureChat_ID = db.getLeagueObjectID(League_ID, "Fixtures")
	if(ctx.channel.id == FixtureChat_ID):
		fixture = db.getFixture(League_ID, fixturenumber)
		teamnames = db.getTeamNames(League_ID)[0]
		message = "Here is Fixture " + str(fixturenumber) + ":\n"
		for match in fixture:
			if match[5] is None:
				message = message + str(match[2])  + ":              " + str(teamnames[match[3]+1]) + " vs " + str(teamnames[match[4]+1]) + "            - Due - " + str(match[7])[0:19] + "\n"
			else:
				message = message + str(match[2]) + ":       **" + str(match[5]) + "**" + "     " + str(teamnames[match[3]+1]) + " vs " + str(teamnames[match[4]+1]) + "     " + "**" + str(match[6]) + "**" + "     - Due - " + str(match[7])[0:19] + "\n"
		await ctx.channel.send(message)
	else:
		await ctx.channel.send("This command must be run in the Fixtures chat of your League")

@client.command(pass_context=True)
@commands.has_role("Manager")
async def submitScore(ctx, Fixture_Pos:int, homescore:int, awayscore:int):
	print("Submit Score")
	guild = client.get_guild(guildid)
	teamID = db.getTeamNumber(ctx.author.id)
	League_ID = db.getLeagueNumber(ctx.author.id)
	LeagueInfo = db.getTeamNames(League_ID)[0]
	match = db.getMatch(League_ID,Fixture_Pos)[0]
	#check if home
	if(teamID == match[3]):
		print("Im home")
		db.submitScore(League_ID,Fixture_Pos,homescore,awayscore)
		awayTeam = match[4]
		awayManager = LeagueInfo[6+awayTeam]
		awayDiscord = discord.utils.get(guild.members, id = int(awayManager))
		channel1 = await ctx.author.create_dm()
		channel2 = await awayDiscord.create_dm()
		scoreMessage = str(Fixture_Pos) + ":       **" + str(homescore) + "**" + "     " + str(LeagueInfo[teamID+1]) + " vs " + str(LeagueInfo[awayTeam+1]) + "     " + "**" + str(awayscore) + "**"
		subID = db.getScoreSubmitID(League_ID,Fixture_Pos)
		await channel1.send("You have submitted a score of:\n" + scoreMessage)
		channel2message = ctx.author.name + " of the team " + str(LeagueInfo[teamID+1]) + " has submitted the score:\n" + scoreMessage + "\nIf you would like to accept type !acceptScore " + str(subID) + "\nIf you would like to decline type !declineScore " + str(subID)
		await channel2.send(channel2message)
	#check if away
	elif(teamID == match[4]):
		print("Im away")
		db.submitScore(League_ID,Fixture_Pos,awayscore,homescore)
		awayTeam = match[3]
		awayManager = LeagueInfo[6+awayTeam]
		awayDiscord = discord.utils.get(guild.members, id = int(awayManager))
		channel1 = await ctx.author.create_dm()
		channel2 = await awayDiscord.create_dm()
		scoreMessage = str(Fixture_Pos) + ":       **" + str(awayscore) + "**" + "     " + str(LeagueInfo[awayTeam+1]) + " vs " + str(LeagueInfo[teamID+1]) + "     " + "**" + str(homescore) + "**"
		subID = db.getScoreSubmitID(League_ID,Fixture_Pos)
		await channel1.send("You have submitted a score of:\n" + scoreMessage)
		channel2message = ctx.author.name + " of the team " + str(LeagueInfo[teamID+1]) + " has submitted the score:\n" + scoreMessage + "\nIf you would like to accept type !acceptScore " + str(subID) + "\nIf you would like to decline type !declineScore " + str(subID)
		await channel2.send(channel2message)
	#neither
	else:
		await ctx.channel.send("This wasn't your match!")

@client.command(pass_context=True)
async def acceptScore(ctx, ID:int):
	guild = client.get_guild(guildid)
	teamID = db.getTeamNumber(ctx.author.id)
	League_ID = db.getLeagueNumber(ctx.author.id)
	manager = db.getManager(League_ID,teamID)
	scoreChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Scores"))
	score = db.getScore(ID)
	if(ctx.author.id == manager):
		if(teamID == Team_1 or teamID == Team_2):
			Team_1 = score[3]
			Team_2 = score[4]
			LeagueInfo = db.getTeamNames(League_ID)[0]
			score_1 = score[5]
			score_2 = score[6]
			Fixture_Pos = score[2]
			db.addFixtureScore(League_ID,Fixture_Pos,score_1,score_2)
			db.deleteScore(League_ID,Fixture_Pos)
			await ctx.channel.send("We will add this to the fixtures now!")
			scoreMessage = str(Fixture_Pos) + ":       **" + str(score_1) + "**" + "     " + str(LeagueInfo[Team_1+1]) + " vs " + str(LeagueInfo[Team_2+1]) + "     " + "**" + str(score_2) + "**"
			await scoreChat.send("The following score has been **accepted** by both managers:\n" + scoreMessage)
		else:
			await ctx.channel.send("Invalid Submission ID")
	else:
		await ctx.channel.send("You are not a manager!")

@client.command(pass_context=True)
async def declineScore(ctx, ID:int):
	guild = client.get_guild(guildid)
	teamID = db.getTeamNumber(ctx.author.id)
	League_ID = db.getLeagueNumber(ctx.author.id)
	LeagueInfo = db.getTeamNames(League_ID)[0]
	scoreChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Scores"))
	score = db.getScore(ID)
	Team_1 = score[3]
	Team_2 = score[4]
	score_1 = score[5]
	score_2 = score[6]
	Fixture_Pos = score[2]
	if(teamID == Team_1 or teamID == Team_2):
		await ctx.channel.send("Thank you, we will let the League know")
		db.deleteScore(League_ID,Fixture_Pos)
		scoreMessage = str(Fixture_Pos) + ":       **" + str(score_1) + "**" + "     " + str(LeagueInfo[Team_1+1]) + " vs " + str(LeagueInfo[Team_2+1]) + "     " + "**" + str(score_2) + "**"
		await scoreChat.send("The following score has been **declined** by " + ctx.author.name + ":\n" + scoreMessage)
	else:
		await ctx.channel.send("Invalid Submission ID")

@client.command(pass_context=True)
@commands.has_role("Manager")
async def makeManager(ctx, user:User):
	guild = client.get_guild(guildid)
	Team_ID = db.getTeamNumber(ctx.author.id)
	League_ID = db.getLeagueNumber(ctx.author.id)
	leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Chat"))
	managerrole = discord.utils.get(guild.roles, name="Manager")
	player = user.mention.replace("<@","").replace(">","")
	print(player)
	#find old manage
	Old_Manager = discord.utils.get(guild.members, id = ctx.author.id)
	New_Manager = discord.utils.get(guild.members, id = int(player))
	print(New_Manager)
	New_Manager_Team_ID = db.getTeamNumber(player)
	New_Manager_League_ID = db.getLeagueNumber(player)
	if(New_Manager_League_ID != 0):
		if(New_Manager_Team_ID != 0):
			if(New_Manager_Team_ID == Team_ID and New_Manager_League_ID == League_ID):
				teamname = db.getTeamName(ctx.author.id)
				db.updateManager(League_ID,Team_ID,New_Manager.id)
				await Old_Manager.remove_roles(managerrole)
				await New_Manager.add_roles(managerrole)
				await leagueChat.send(teamname + "'s manager <@" + str(Old_Manager.id) + "> has resigned and <@" + str(New_Manager.id) + "> has replaced them in the role!")
			else:
				await ctx.channel.send("This player is not in your team")
		else:
			await ctx.channel.send("This player is not in a Team")
	else:
		await ctx.channel.send("This player is not in a League")

@client.command(pass_context=True)
@commands.has_role("Manager")
async def kick(ctx, user:User):
	guild = client.get_guild(guildid)
	Team_ID = db.getTeamNumber(ctx.author.id)
	League_ID = db.getLeagueNumber(ctx.author.id)
	leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Chat"))
	player = user.mention.replace("<@","").replace(">","")
	print(player)
	Old_Manager = discord.utils.get(guild.members, id = ctx.author.id)
	New_Manager = discord.utils.get(guild.members, id = int(player))
	print(New_Manager)
	New_Manager_Team_ID = db.getTeamNumber(player)
	New_Manager_League_ID = db.getLeagueNumber(player)
	if(New_Manager_League_ID != 0):
		if(New_Manager_Team_ID != 0):
			if(New_Manager_Team_ID == Team_ID and New_Manager_League_ID == League_ID):
				teamname = db.getTeamName(ctx.author.id)
				leagueRole = discord.utils.get(guild.roles, id=db.getLeagueObjectID(League_ID,"Role"))
				await New_Manager.remove_roles(leagueRole)
				db.deletePlayer(New_Manager.id)
				await leagueChat.send("<@" + str(New_Manager.id) + ">'s contract has been terminated from " + teamname + "!")
				DMNotice = await New_Manager.create_dm()
				await DMNotice.send("Sorry to inform you but your contract for the team " + teamname + " has been terminated!")
			else:
				await ctx.channel.send("This player is not in your team")
		else:
			await ctx.channel.send("This player is not in a Team")
	else:
		await ctx.channel.send("This player is not in a League")

@client.command(pass_context=True)
async def table(ctx):
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueNumber(ctx.author.id)
	leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Chat"))
	scores = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Scores"))
	fixtures = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Fixtures"))
	team = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Team"))
	if(ctx.channel.id == leagueChat.id or ctx.channel.id == scores.id or ctx.channel.id == fixtures.id or ctx.channel.id == team.id):
		fixturetable = "```yaml\n" + db.calculateTable(League_ID) + "\n```"
		await ctx.channel.send(fixturetable)
	else:
		await ctx.channel.send("This command can only be used within your League!")

@client.command(pass_context=True)
async def leaveLeague(ctx):
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueNumber(ctx.author.id)
	Team_ID = db.getTeamNumber(ctx.author.id)
	leagueRole = discord.utils.get(guild.roles, id=db.getLeagueObjectID(League_ID,"Role"))

	if(League_ID != 0):
		manager = db.getManager(League_ID,Team_ID)
		if(ctx.author.id == manager):
			await ctx.channel.send("You are a manager so you cannot leave the league until you transfer ownership.")
		else:
			Member = discord.utils.get(guild.members, id = int(ctx.author.id))
			await Member.remove_roles(leagueRole)
			db.deletePlayer(ctx.author.id)
	else:
		await ctx.channel.send("You are not part of a League!")

#Person leaving
@client.event
async def on_member_remove(member):
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueNumber(member.id)
	if(League_ID != 0):
		leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Chat"))
		await leagueChat.send(str(member.name) + " has left the League, if they where a manager please contact staff and open a ticket under tech support.")
		db.deletePlayer(member.id)

@client.command(pass_context=True)
async def toss(ctx):
	rnd = random.randint(1,3)
	if rnd == 1:
		await ctx.channel.send("Heads!")
	else:
		await ctx.channel.send("Tails!")

@client.command(pass_context=True)
@commands.has_role("Staff")
async def staffSetManager(ctx, user:User, *, Team:str):
	guild = client.get_guild(guildid)
	League_ID = db.getLeagueID(ctx.channel.id,"Chat")
	print(League_ID)
	print(Team)
	Team_ID = db.getTeamIDByName(League_ID,Team)
	leagueChat = discord.utils.get(guild.channels, id=db.getLeagueObjectID(League_ID,"Chat"))
	managerrole = discord.utils.get(guild.roles, name="Manager")
	player = user.mention.replace("<@","").replace(">","")
	print(player)
	Teams = db.getTeamNames(League_ID)
	Old_Manager_ID = Teams[0][6+Team_ID]
	Old_Manager = discord.utils.get(guild.members, id = Old_Manager_ID)
	New_Manager = discord.utils.get(guild.members, id = int(player))
	print(New_Manager)
	New_Manager_Team_ID = db.getTeamNumber(player)
	New_Manager_League_ID = db.getLeagueNumber(player)
	if(New_Manager_League_ID != 0):
		if(New_Manager_Team_ID != 0):
			if(New_Manager_Team_ID == Team_ID and New_Manager_League_ID == League_ID):
				teamname = Team
				db.updateManager(League_ID,Team_ID,New_Manager.id)
				await Old_Manager.remove_roles(managerrole)
				await New_Manager.add_roles(managerrole)
				await leagueChat.send(teamname + "'s manager <@" + str(Old_Manager.id) + "> has resigned and <@" + str(New_Manager.id) + "> has replaced them in the role!")
			else:
				await ctx.channel.send("This player is not in your team")
		else:
			await ctx.channel.send("This player is not in a Team")
	else:
		await ctx.channel.send("This player is not in a League")

@client.command(pass_context=True)
@commands.has_role("Staff")
async def viewInvites(ctx):
	fixturetable = "```yaml\n" + db.getInvites() + "\n```"
	await ctx.channel.send(fixturetable)


client.run(KEY)
