import discord
import random
from discord.ext import commands
from discord import Embed
from requests import get
import asyncio
import datetime
from datetime import datetime
import os


owner = 808039521328693268


Token = os.environ['TOKEN']

client = commands.Bot(command_prefix="o.", description="I'm here for your needs.")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="o.help"))
    print(f'{client.user.name} is ready')
    print(f'with the id: {client.user.id}')
  #  client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')
    await ctx.send(round(client.latency * 1000))

#@client.command()
#async def av(ctx,*, avamember):
#    user = client.get_user(avamember)
#    await ctx.send(f"{user.avatar_url}")

@client.command(aliases=['Say', 'say'])
async def speak(ctx, *, text: str):
    message = ctx.message
    await message.delete()
    await ctx.send(f"{text}")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, que):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt',
                 'Yes - definitely.',
                 'you may rely on it.',
                 'As i see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Repy hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Dont count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.reply(f'QUESTION: {que}\nANSWER: {random.choice(responses)} ')


@client.command()
async def ip(ctx):
  ip = get('https://api.ipify.org').text
  embed=discord.Embed(title="My IP Address!", url="https://api.ipify.org", description="Hi! Click the link to see your IP address! Otanoids current IP address is: {}".format(ip), color=0x28c3c0) 
  embed.set_footer(text="Made by Miata♥ and Wir3d")
  await ctx.reply(embed=embed)

@client.command(pass_context=True)
async def av(ctx, *, member: discord.Member):
  pfp = member.avatar_url
  
  embed = discord.Embed(title="Profile picture.", color=0x28c3c0)
  embed.set_image(url=pfp)
  await ctx.send(embed=embed) 

@client.command(pass_context=True)
async def nick(ctx, member: discord.Member, nick: str):
    await member.edit(nick=nick)
    await ctx.send(f'New nickname for {member.mention}!')

@client.command()
async def reverse(ctx, *, msg: str):
  await ctx.send(msg[::-1])

@client.command()
async def nothing(ctx):
  await ctx.send('_ _')

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time,* , reminder ):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 60:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, {ctx.author.mention} asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)

@client.command(pass_context = True)
async def poll(self, ctx, question, *, options: str, message: str):
  author = ctx.message.author
  server = ctx.message.server
  
  if not author.server_permissions.manage_messages: return await self.bot.say(DISCORD_SERVER_ERROR_MSG)
  
  if len(options) <= 1:
    await self.bot.say("```Error! A poll must have more than one option.```")
    return
    
    if len(options) > 2:
      await self.bot.say("```Error! Poll can have no more than two options.```")
      return

    if len(options) == 2 and options[0] == "yes" and options[1] == "no":
      reactions = ['👍', '👎']
    else:
      reactions = ['👍', '👎']
      
      description = []
      for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)
        
        embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))
        react_message = await self.bot.say(embed = embed)
        for reaction in reactions[:len(options)]:
          await self.bot.add_reaction(react_message, reaction)
          embed.set_footer(text='Poll ID: {}'.format(react_message.id))
          
          await self.bot.edit_message(react_message, embed=embed)

client.run(Token)
