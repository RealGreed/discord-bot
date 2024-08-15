from nextcord.ext import commands, tasks
import nextcord
import os
import datetime
import asyncio
import pytz
import openai

openai.api_key = os.environ['AI_TOKEN']

meeting_channel = 1228883489638842419
intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

keyword_links = {
    "gamelore": "https://docs.google.com/document/d/1zqPAb4B5TxwWmvUGShKRrLluRE0_QnxEcWS-DzziW4E/edit#heading=h.gt93xjnmmbz",
    "divinelore": "https://docs.google.com/document/d/1RbRWpLsR42dbJecnHyU23-jhRHlcHaXBTMTlTYiIVZk/edit#heading=h.37vf2hug3krk",
}

# tasks
items = []
completed_items =[]

@bot.command()
async def add(ctx, *, task:str):
    print(f"Added {task} to the items")
    # Adds the task to the list
    task.append(task)
    await display_items(ctx)

@bot.command()
async def completed(ctx, *, task:str):
    # mark as completed
    if task in items:
        items.remove(task)
        completed_items.append(task)
        await display_items(ctx)
    else:
        await ctx.send(f'Task "{task}" not found in the list.')

@bot.command()
async def show(ctx):
    print("Showing the list")
    if completed_items:
        completed_message = "Completed Tasks:\n" + "\n".join(completed_items)
    else:
        completed_message = "No completed tasks yet."
    await ctx.send(completed_message)

@bot.command()
async def delete(ctx, *, task:str):
    if task in items:
        items.remove(task)
        await display_items(ctx)
        await ctx.send(f'Task"{task}" deleted from the current tasks list.')
    elif task in completed_items:
        completed_items.remove(task)
        await ctx.send(f'Task"{task} deleted from the completed tasks lsit.')
    else:
        await ctx.send(f'Task"{task}" not found in either the current or completed tasks list.')
        
async def display_items(ctx):
    print("Displaying the items")
    """Displays the current lists of tasks"""
    if items:
        task_message = "Current Tasks:\n" + "\n".join(items)
    else:
        task_message = "No tasks in the list."
    await ctx.send(task_message)

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
        
async def meeting_reminder():
    channel = bot.get_channel(meeting_channel)
    await channel.send("@here MEETING IS IN 30 MINUTES!")

async def meeting_message():
    channel = bot.get_channel(meeting_channel)
    await channel.send("@here THE MEETING IS BEING HELD IN #MEETING!")

# Handles meeting reminders
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
