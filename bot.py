from nextcord.ext import commands
import nextcord
import os
import datetime
import asyncio
import pytz

bot = commands.Bot(command_prefix="dog ")

async def meeting_reminder():
    channel = bot.get_channel(1039284243697762467)
    await channel.send("@here MEETING IS IN 30 MINUTES!")

async def meeting_message():
    channel = bot.get_channel(1039284243697762467)
    await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")

async def check_time_and_send_messages():
    cst = pytz.timezone('America/Chicago')  # Central Standard Time
    while True:
        print("Checking time...")
        now = datetime.datetime.now(cst)
        print("Current time:", now)

        # only runs on Wednesdays
        if now.weekday() == 2:
            reminder_time = cst.localize(datetime.datetime(now.year, now.month, now.day, 20, 30))
            meeting_time = cst.localize(datetime.datetime(now.year, now.month, now.day, 21, 0))
            print("Reminder time: ", reminder_time)
            print("Meeting time: ", meeting_time)
            
            if now >= meeting_time:
                print("Sending meeting message...")
                await meeting_message()
            elif now >= reminder_time:
                print("Sending meeting reminder...")
                await meeting_reminder()

        # Sleep for 1 hour before checking again
        print("Sleeping for 25 minutes...")
        await asyncio.sleep(900)  # 3600 seconds = 1 hour

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # Start the loop to check time and send messages
    bot.loop.create_task(check_time_and_send_messages())

if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
