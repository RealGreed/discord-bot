from nextcord.ext import commands
import nextcord
import os
import datetime
import asyncio
import pytz

bot = commands.Bot(command_prefix="bot ")

async def respond_doc_call():
    while True:
        bot.add_listener('Meeting Logs')
        channel = bot.get_channel(1040065014867968041)
        await channel.send("https://docs.google.com/document/d/1DNqomQuh7jjDR28-u0PZR3kddp7T6bV8lLgn8Qho9_g/edit")
        
async def meeting_reminder():
    channel = bot.get_channel(1228883489638842419)
    await channel.send("@here MEETING IS IN 30 MINUTES!")

async def meeting_message():
    channel = bot.get_channel(1228883489638842419)
    await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")

async def check_time_and_send_messages():
    cst = pytz.timezone('America/Chicago')  # Central Standard Time
    reminder_sent = False  # Variable to track if reminder has been sent for the day
    meeting_sent = False # Variable to track if meeting has been sent for the day
    while True:
        print("Checking time...")
        now = datetime.datetime.now(cst)
        print("Current time (CST):", now)

        # Reset reminder_sent if it's a new day
        if 1 >=now.hour >= 00 and 2 >= now.minute >= 0:
            reminder_sent = False
            meeting_sent = False

        # only runs on Wednesdays and if reminder hasn't been sent for the day
        if (now.weekday() == 2 or now.weekday() == 5) and not reminder_sent:
            if now.hour >= 20 and now.minute >= 30:
                print("Sending meeting reminder...")
                await meeting_reminder()
                reminder_sent = True  # Set reminder_sent to True after sending reminder
        else:
            reminder_sent = False

         # only runs on Wednesdays and Saturday if meeting has not been sent for the day
        if (now.weekday() == 2 or now.weekday() == 5) and not meeting_sent:
            if now.hour >= 21 and now.minute >= 00:
                print("Sending meeting message...")
                await meeting_message()
                meeting_sent = True  # Set meeting_sent to True after sending message
        else:
            meeting_sent = False

        # Sleep for 1 minute before checking again
        print("Sleeping for 15 minute...")
        await asyncio.sleep(900)  # 60 seconds = 1 minute

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # Start the loop to check time and send messages
    bot.loop.create_task(check_time_and_send_messages())

if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
