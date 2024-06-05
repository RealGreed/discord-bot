from nextcord.ext import commands, tasks
import nextcord
import os
import datetime
import asyncio
import pytz
import openai

openai.api_key = os.environ['AI_TOKEN']

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="bot ", intents=intents)

keyword_links = {
    "gamelore": "https://docs.google.com/document/d/1zqPAb4B5TxwWmvUGShKRrLluRE0_QnxEcWS-DzziW4E/edit#heading=h.gt93xjnmmbz",
    "divinelore": "https://docs.google.com/document/d/1RbRWpLsR42dbJecnHyU23-jhRHlcHaXBTMTlTYiIVZk/edit#heading=h.37vf2hug3krk",
}

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

@bot.event
async def on_message(message):
    # Don't let the bot respond to its own messages
    if message.author == bot.user:
        return
    
    # Check for keywords and respond with links
    for keyword, link in keyword_links.items():
        if keyword.lower() in message.content.lower():
            await message.channel.send(f"{message.author.mention}, you mentioned '{keyword}'. Here is a reference link: {link}")
            break  # Optionally, stop checking after the first match

    # Check if the message is appropriate
    if not is_message_appropriate(message.content):
        await message.channel.send(f"{message.author.mention}, you have been banned for inappropriate language.")
        await message.author.ban(reason="Inappropriate language")
        return
        
async def meeting_reminder():
    channel = bot.get_channel(1228883489638842419)
    await channel.send("@here MEETING IS IN 30 MINUTES!")

async def meeting_message():
    channel = bot.get_channel(1228883489638842419)
    await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")

@tasks.loop(minutes=1)
async def check_time_and_send_messages():
    cst = pytz.timezone('America/Chicago')
    now = datetime.datetime.now(cst)

    if now.hour == 00 and now.minute <= 2:
        print ("Resetting reminder and meeting.")
        reminder_sent = False
        meeting_sent = False

    if now.hour == 0 and now.minute <= 2:
        check_time_and_send_messages.reminder_sent = False
        check_time_and_send_messages.meeting_sent = False

    if (now.weekday() == 2 or now.weekday() == 5) and not check_time_and_send_messages.reminder_sent:
        if now.hour == 20 and now.minute >= 30:
            await meeting_reminder()
            check_time_and_send_messages.reminder_sent = True

    if (now.weekday() == 2 or now.weekday() == 5) and not check_time_and_send_messages.meeting_sent:
        if now.hour == 21 and now.minute <= 1:
            await meeting_message()
            check_time_and_send_messages.meeting_sent = True

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    check_time_and_send_messages.reminder_sent = False
    check_time_and_send_messages.meeting_sent = False
    check_time_and_send_messages.start()

if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
