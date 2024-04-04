from nextcord.ext import commands
import nextcord
import os
import datetime
import asyncio

bot = commands.Bot(command_prefix="dog ")

async def meeting_reminder():
    channel = bot.get_channel(1039284243697762467)
    await channel.send("@here MEETING IS IN 30 MINUTES!")

async def meeting_message():
    channel = bot.get_channel(1039284243697762467)
    await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")

async def check_time_and_send_messages():
    while True:
        now = datetime.datetime.now()

        # only runs on Wednesdays
        if now.weekday() == 2:
            reminder_time = now.replace(hour=20, minute=30)
            meeting_time = now.replace(hour=21, minute=0)
            
            if now >= meeting_time:
                await meeting_message()
            elif now >= reminder_time:
                await meeting_reminder()

        # Sleep for 1 hour before checking again
        await asyncio.sleep(3600)  # 3600 seconds = 1 hour

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # Start the loop to check time and send messages
    bot.loop.create_task(check_time_and_send_messages())

if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
