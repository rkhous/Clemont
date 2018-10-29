import discord
from discord.ext import commands
from bot import *
from config import *
from requirements import *
from geopy.distance import great_circle

bot = commands.Bot(command_prefix='//')

@bot.event
async def on_ready():
    print('-' * 15)
    print('Clemont is now online')
    print('-' * 15)

@bot.event
async def on_message(message):
    if str(message.author.id) == clembot_id and clembot_search_term in str(message.content).lower():
        m = Message(message.embeds)
        data = m.process_message()
        n = Notification(data=data)
        notify_users = n.get_user_info()
        if len(notify_users) == 0:
            pass
        else:
            for n in notify_users:
                if n[2] == '0' and n[3] == '0':
                    raid_embed = discord.Embed(
                        title='Click for Directions!',
                        url=data['url'],
                        description='A raid you asked to be notified about has appeared!'
                    )
                    raid_embed.set_image(url='http://www.pokestadium.com/sprites/xy/{}.gif'.format(data['pokemon_name'].lower()))
                    raid_embed.set_footer(text='Created by github.com/rkhous', icon_url='https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png')
                    await bot.send_message(destination=discord.User(id=n[0]), embed=raid_embed)
                    print('Notifying a user for a raid, regardless of distance.')
                else:
                    raid_location = (float(data['lat']), float(data['lon']))
                    user_location = (float(n[2]), float(n[3]))
                    distance = great_circle(user_location, raid_location).miles
                    if distance <= n[4]:
                        raid_embed = discord.Embed(
                            title='Click for Directions!',
                            url=data['url'],
                            description='A raid you asked to be notified about has appeared\n'
                                        'and is only {} miles from you!'.format(round(distance,2))
                        )
                        raid_embed.set_image(url='http://www.pokestadium.com/sprites/xy/{}.gif'.format(data['pokemon_name'].lower()))
                        raid_embed.set_footer(text='Created by github.com/rkhous',icon_url='https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png')
                        await bot.send_message(destination=discord.User(id=n[0]), embed=raid_embed)
                        print('Notifying a user of a raid based on distance')
                    else:
                        pass
                        print('A user was too far from a raid they wanted to be notified about.')
    else:
        pass
    await bot.process_commands(message)

@bot.command(pass_context=True, aliases='n')
async def notify(ctx, name=None, location=None, distance=0):
    try:
        if name is None and location is None and distance == 0:
            await bot.say('{}, please use the following command to be added to the notification list:\n'
                          '```//notify <pokemon> <lat,lon> <miles from you>```'
                          .format(ctx.message.author.mention))
        elif str(name).lower() not in pokemon:
            await bot.say('{}, {} is not a Pokémon!'.format(ctx.message.author.mention, name.capitalize()))
        elif ctx.message.server is None:
            db = Database(user_id=ctx.message.author.id, poke_name=name.capitalize(), location=location, distance=distance)
            await bot.say(db.add_to_notifications())
        else:
            await bot.say("{}, your message has been deleted for privacy reasons. "
                          "Let's move this to Direct Messaging instead.".format(ctx.message.author.mention))
    except ValueError:
        await bot.say('{}, something went wrong and it is likely caused by using the command incorrectly.\n'
                      'Please make sure lat,lon has no space in between!'.format(ctx.message.author.mention))
    finally:
        await bot.delete_message(ctx.message)

@bot.command(pass_context=True, aliases='r')
async def remove(ctx, name=None):
    if name is None:
        await bot.say('{}, please use the following command to remove a notification from your list:\n'
                      '```//remove <pokemon>```'.format(ctx.message.author.mention))
    elif str(name).lower() not in pokemon:
        await bot.say('{}, {} is not a Pokémon'.format(ctx.message.author.mention, name.capitalize()))
    else:
        db = Database(user_id=ctx.message.author.id, poke_name=name.capitalize(), location=None, distance=0)
        await bot.say(db.remove_from_notifications())

bot.run(token)