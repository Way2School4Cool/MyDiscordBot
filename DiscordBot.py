'''
Caleb McGraw
5/30/21

Current iteration published: 8/3/21
'''
import os
import random
import discord
import csv
#import pandas
import Magic_Program
import WatchMTGPrices
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='*', intents=intents)

client = discord.Client()

'''
@bot.event
async def on_message(message):
	if message.author.id == 235055239479164931:
		output = WatchMTGPrices.checkPrices()
		if (output != ""):
			await message.channel.send(output)
		else:
			print("No Changes")
	await bot.process_commands(message)
'''

@bot.command(name="MTGPack", help="Simulate MTG pack ex. *MTGPack ZEN")
async def getPack(ctx, packName = "ZEN"):
	await ctx.send(Magic_Program.generateBooster(packName))


@bot.command(name = "MTGWatch", help="*Currently on pause* Watch a 'Star City' product, enter a url to watch")
async def MTGPriceWatcher(ctx, url):

	#send the product setter the request		
	MTGProduct = WatchMTGPrices.SetProduct(url, member = ctx.message.author)

	#check responce from the setter
	if MTGProduct == None:
		await ctx.send("Error, Link Incorrect?")

	elif MTGProduct == "redundant":
		await ctx.send("Already in the list")

	else:
		await ctx.send(str(MTGProduct.requestor) + ": " + MTGProduct.name + " is currently " + str(MTGProduct.price))


@bot.command(name="whois", help="Lookup info on users")
async def userinfo(ctx, member: discord.Member = None):
	if not member:  # if member is not mentioned
		member = ctx.message.author  # set member as the author
	roles = [role for role in member.roles[1:]]
	embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
						  title=f"User Info - {member}")
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.author}")

	embed.add_field(name="ID:", value=member.id)
	embed.add_field(name="Display Name:", value=member.display_name)

	embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

	#embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
	embed.add_field(name="Highest Role:", value=member.top_role.mention)
	print(member.top_role.mention)
	await ctx.send(embed=embed)

@bot.command(name="based", help="uptick user's based counter")
async def basedTracker(ctx, member: discord.Member = None):
	# if member is not mentioned
	if not member:
		await ctx.send("Please specify a based user")
	
	else:
		output = ""
		userList = []
		userCount = []

		#load csv into 2 lists in memory
		with open("BasedCount.csv", mode="r", newline="") as BasedFile:
			reader = csv.reader(BasedFile)
			for user in reader:
				userList.append(user[0])
				userCount.append(user[1])

		#re-write the csv, but incriment the specified user
		with open("BasedCount.csv", mode="w", newline="") as BasedFile:
			writer = csv.writer(BasedFile)
			for user in range(len(userList)):
				if userList[user][0:-5] == member.name:
					writer.writerow([userList[user], (int(userCount[user]) + 1)])
					output = userList[user] + " based count is NOW: " + str(int(userCount[user]) + 1)
				else:
					writer.writerow([userList[user], userCount[user]])
		
		#output the incrimented user
		await ctx.send(output)

@bot.command(name="baseCount", help="Check a user's current based count")
async def basedTracker(ctx, member: discord.Member = None):
	if not member:  # if member is not mentioned
		member = ctx.message.author  # set member as the author

	#find mentioned user, and output their current score		
	with open("BasedCount.csv", mode="r", newline="") as BasedFile:
		reader = csv.reader(BasedFile)
		for user in reader:
			if user[0][0:-5] == member.name:
				output = (user[0] + " based count: " + str(user[1]))
				break
			else:
				output = "Member not found"

	await ctx.send(output)

@bot.command(name="baseReset", help="Reset ANOTHER USER'S score")
async def basedTracker(ctx, member: discord.Member = None):
	if not member:  # if member is not mentioned
		await ctx.send("Please select a user (You may not select yourself)")

	#a member may not reset their own count
	elif member == ctx.message.author:
		await ctx.send("You may not reset your own count")

	#if a member was mentioned that wasnt the author:
	else:
		output = ""
		userList = []
		userCount = []

		#load csv into 2 lists in memory
		with open("BasedCount.csv", mode="r", newline="") as BasedFile:
			reader = csv.reader(BasedFile)
			for user in reader:
				userList.append(user[0])
				userCount.append(user[1])

		#re-write the csv, but change the mentioned user's score to zero
		with open("BasedCount.csv", mode="w", newline="") as BasedFile:
			writer = csv.writer(BasedFile)
			for user in range(len(userList)):
				if userList[user][0:-5] == member.name:
					writer.writerow([userList[user], 0])
					output = userList[user] + " based count has been reset to zero"
				else:
					writer.writerow([userList[user], userCount[user]])

	#output changed user
	await ctx.send(output)



@bot.event
async def on_ready():
	membersToAdd = []

	
	for guild in bot.guilds:
		print(guild)

		#for every member in every guild:
		for member in guild.members:
			user = ""
			print(member)
	
			#check if they are already in the csv:
			with open("BasedCount.csv", mode="r", newline="") as BasedFile:
				reader = csv.reader(BasedFile)
				for csvUsers in reader:
					
					#if so, do nothing
					if csvUsers[0][0:-5] == member.name:
						user = member
						break
				
				#if not, add them to a list of members to add
				if user == "":
					membersToAdd.append(member)
					user = "none"
					
	#append the users mentioned to the list
	with open("BasedCount.csv", mode="a+", newline="") as BasedFile:
		writer = csv.writer(BasedFile)
		for addition in membersToAdd:
			writer.writerow([addition, 0])

bot.run(TOKEN)
