from nextcord.ext import commands
import nextcord
import os
import datetime
import asyncio
import pytz
import discord
import openai

bot = commands.Bot(command_prefix="bot ")
openai.api_key = os.environ('AI_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

def is_message_appropriate(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a moderation assistant. Classify the following message as appropriate or inappropriate."},
            {"role": "user", "content": f"Message: '{message}'"}
        ],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )
    result = response.choices[0].message['content'].strip().lower()
    return "appropriate" in result

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't let the bot respond to its own messages
    if message.author == client.user:
        return

    # Check if the message is appropriate
    if not is_message_appropriate(message.content):
        await message.channel.send(f"{message.author.mention}, you have been banned for inappropriate language.")
        await message.author.ban(reason="Inappropriate language")
        return

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

async def check_time_and_send_messages(reminder_sent, meeting_sent):
    cst = pytz.timezone('America/Chicago')  # Central Standard Time
    while True:
        print("Checking time...")
        now = datetime.datetime.now(cst)
        print("Current time (CST):", now)

        # Reset reminder_sent if it's a new day
        if now.hour == 00 and now.minute <= 2:
            print ("Resetting reminder and meeting.")
            reminder_sent = False
            meeting_sent = False

        # only runs on Wednesdays and if reminder hasn't been sent for the day
        if (now.weekday() == 2 or now.weekday() == 5) and not reminder_sent:
            if now.hour == 20 and now.minute >= 30:
                print("Sending meeting reminder...")
                await meeting_reminder()
                reminder_sent = True  # Set reminder_sent to True after sending reminder

         # only runs on Wednesdays and Saturday if meeting has not been sent for the day
        if (now.weekday() == 2 or now.weekday() == 5) and not meeting_sent:
            if now.hour == 21 and now.minute <= 1:
                print("Sending meeting message...")
                await meeting_message()
                meeting_sent = True  # Set meeting_sent to True after sending message
                
        # Sleep for 1 minute before checking again
        print("Sleeping for a minute...")
        await asyncio.sleep(60)  # 60 seconds = 1 minute

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # Start the loop to check time and send messages
    reminder_sent = False
    meeting_sent = False
    bot.loop.create_task(check_time_and_send_messages(reminder_sent, meeting_sent))

if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])

