from nextcord.ext import commands
import requests, json, random, datetime, asyncio
import os

bot = commands.Bot(command_prefix="dog ")

async def meeting_reminder():
	channel = bot.get_channel(1039284243697762467)
	await channel.send("@here MEETING IS IN 30 MINUTES!")

	
async def meeting_message():
	channel = bot.get_channel(1039284243697762467)

	await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")
		
@bot.event
async def on_ready():
	print(f"Loggined in as: {bot.user.name}")
	now = datetime.datetime.now()

	# only runs on wednesdays
	if now.weekday() != 2:
		return
	
	reminder_time = now.replace(hour=20, minute=30)
	meeting_time = now.replace(hour=21, minute=0)
	
	if now >= meeting_time:
		await meeting_message()
	elif now >= reminder_time:
		await meeting_message()
	else:
		return

if __name__ == '__main__':
	bot.run(os.environ["DISCORD_TOKEN"])