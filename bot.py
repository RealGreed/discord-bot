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
	reminder_time = now.replace(hour=22, minute=8)
	meeting_time = now.replace(hour=22, minute=10)
	
	if now < reminder_time:
		await meeting_reminder()
	elif reminder_time <= now < meeting_time:
		await meeting_message()
	else:
		print("Meeting time has passed.")

if __name__ == '__main__':
	bot.run(os.environ["DISCORD_TOKEN"])