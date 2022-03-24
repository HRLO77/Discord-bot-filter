import disnake
from disnake.ext import commands, tasks
from explicit_data import *
TOKEN = 'TOKEN'


def convert_to_list(string):
    cache = ''
    data = []
    for i in string.replace(' ', ''):
        if i == ',':
            data.append(cache)
            cache = ''
        else:
            cache = f'{cache}{i}'
    data.append(cache)
    return data


bot = commands.Bot(command_prefix='>', case_insensitive=True, intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f'We have logged on as {bot.user}({bot.user.id}) with a latency of {round(bot.latency * 1000)} ms.')


class filtering(commands.Cog):
  
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener("on_member_join")
  async def on_member_join(self, member: disnake.Member):
      if member.public_flags.spammer:
          await member.kick(reason='Marked as spammer.')
          return
      await member.send(f'{member.mention} Welcome to **{member.guild.name}**!')
      await member.send(':wave:')
       
      
  @commands.Cog.listener("on_message")
  async def on_message(self, message: disnake.Message):
      global filtering
        if not(message.guild is None):
            try:
                filtering[str(message.guild.id)]
            except KeyError:
                filtering[str(message.guild.id)] = (1, 2)
        async def syspurgeban(member_id, limit=10, bulk: bool = False):
            list_messages = []
            messages = 0
            async for i in message.channel.history(limit=None):
                if messages >= limit:
                    if bulk:
                        await message.channel.delete_messages(list_messages)
                    return
                if i.author.id == member_id:
                    if not(bulk):
                        messages += 1
                        await i.delete()
                    elif bulk:
                        messages += 1
                        list_messages.append(i)
                else:
                    continue

        def check_for_spam(m):
            return m.author == message.author or m.content.lower().replace(' ', '') in message.content.lower().replace(' ', '') or message.content.lower().replace(' ', '') in m.content.lower().replace(' ', '') or len(m.mentions) > round(7 / filtering[str(m.guild.id)][1]) or (filtering[str(m.guild.id)][1] > 2 and m.content.isupper())
        if message.guild is None:
            return
        test = str(str(message.content).replace(' ', '')).lower()
        if message.author.bot:
            return
        else:
            pass
        cache = ''
        if (filtering[str(message.guild.id)][1]) == 1:
            count = 0
            for index, value in enumerate(test):
                if value == cache:
                    count += 1
                if value.isupper():
                    count += 1
                if not(value.isascii()):
                    count += 1
                cache = value
            count -= 1
            if len(test) > 950 or count > 27 or len(message.mentions) > round(7 / filtering[str(message.guild.id)][1]):
                await message.delete()
        elif (filtering[str(message.guild.id)][1]) == 2:
            count = 0
            for index, value in enumerate(test):
                if value == cache:
                    count += 1
                if not (value.lower() in valid_chars):
                    count += 1
                if value.isupper():
                    count += 1
                if not(value.isascii()):
                    count += 1
                cache = value
            count -= 1
            if len(test) > 450 or count > 15 or len(message.mentions) > round(7 / filtering[str(message.guild.id)][1]):
                await syspurgeban(message.author.id, 10, 1)
        elif (filtering[str(message.guild.id)][1]) == 3:
            count = 0
            for index, value in enumerate(test):
                if value == cache:
                    count += 1
                if value.lower() in special_chars:
                    count += 1
                if not (value.lower() in valid_chars):
                    count += 0.5
                if not(value.isascii()):
                    count += 2
                cache = value
            count -= 1
            if len(test) > 195 or count > 11 or len(message.mentions) > round(7 / filtering[str(message.guild.id)][1]) or message.content.isupper():
                await syspurgeban(message.author.id, 25, 1)
                await message.author.timeout(duration=300.0, reason='Spam')
                await message.author.send(
                    f'{message.author.mention} you\'ve been muted in **{message.guild}** for spamming for **5** minutes.')
        elif (filtering[str(message.guild.id)][1]) == 4:
            count = 0
            for index, value in enumerate(test):
                if value == cache:
                    count += 1
                if value in special_chars:
                    count += 1
                if not (value in valid_chars):
                    count += 1
                if value.isupper():
                    count += 1
                if not(value.isascii()):
                    count += 1
                cache = value
            count -= 1
            if len(test) > 90 or count > 5 or len(message.mentions) > round(7 / filtering[str(message.guild.id)][1]) or message.content.isupper():
                await syspurgeban(message.author.id, 30, 1)
                await message.author.timeout(duration=600.0, reason='Spam')
                await message.author.send(
                    f'{message.author.mention} you\'ve been muted in **{message.guild}** for spamming for **10** minutes.')
        if (filtering[str(message.guild.id)][0]) == 1:
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data2):
                await message.delete()
        elif (filtering[str(message.guild.id)][0]) == 2:
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data3):
                await message.delete()
        elif (filtering[str(message.guild.id)][0]) == 3:
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data4):
                await message.delete()
            for i in filter4:
                test = test.replace(i, '*')
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data4):
                await message.delete()
        elif (filtering[str(message.guild.id)][0]) == 4:
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data5):
                await message.delete()
            for i in filter5:
                test = test.replace(i, '*')
            if profanity.contains_profanity(test) or any(i in test for i in explicit_data5):
                await message.delete()
        # syspurgeban(message.author.id, 10, 1)
        # await message.author.timeout(duration=60.0, reason='Spam')
        # await message.author.send(
        #     f'{message.author.mention} you\'ve been muted in **{message.guild}** for spamming for **60** seconds.')
        # await message.channel.send(f'{message.author.mention} please do not spam.')
        if (filtering[str(message.guild.id)][1]) == 1:
            try:
                await self.bot.wait_for('message', timeout=1, check=check_for_spam)
            except asyncio.exceptions.TimeoutError:
                pass
            else:
                await syspurgeban(message.author.id, 5, 1)
        elif (filtering[str(message.guild.id)][1]) == 2:
            try:
                await self.bot.wait_for('message', timeout=2, check=check_for_spam)
            except asyncio.exceptions.TimeoutError:
                pass
            else:
                await syspurgeban(message.author.id, 15, 1)
        elif (filtering[str(message.guild.id)][1]) == 3:
            try:
                await self.bot.wait_for('message', timeout=8.5, check=check_for_spam)
            except asyncio.exceptions.TimeoutError:
                pass
            else:
                await syspurgeban(message.author.id, 25, 1)
                await message.author.timeout(duration=300.0, reason='Spam')
                await message.author.send(
                    f'{message.author.mention} you\'ve been muted in **{message.guild}** for spamming for **5** minutes.')
        elif (filtering[str(message.guild.id)][1]) == 4:
            try:
                await self.bot.wait_for('message', timeout=15, check=check_for_spam)
            except asyncio.exceptions.TimeoutError:
                pass
            else:
                await syspurgeban(message.author.id, 30, 1)
                await message.author.timeout(duration=600.0, reason='Spam')
                await message.author.send(
                    f'{message.author.mention} you\'ve been muted in **{message.guild}** for spamming for **10** minutes.')

                
      @commands.command(aliases=('spam_filter', 'spam_check'), description='Sets spam filter for current guild.')
    @commands.has_permissions(manage_server=True)
    async def spam(self, ctx, value):
        global filtering
        try:
            filtering[str(ctx.guild.id)]
        except KeyError:
            filtering[str(ctx.guild.id)] = (1, 1)
        if int(value) and int('-1') < int(value) < 5 or int(value) == 0:
            filtering[str(ctx.guild.id)] = (int(value), (filtering[str(ctx.guild.id)])[1])
        else:
            raise ValueError('Invalid value for "spam_check".')
        await ctx.send(f'Spam filter level has been set to {value}.')


    @commands.command(aliases=('content_filter', 'content_check', 'swear_check', 'profanity_filter', 'profanity_check'), description='Sets swear filter for current guild.')
    @commands.has_permissions(manage_server=True)
    async def content(self, ctx, value):
        global filtering
        try:
            filtering[str(ctx.guild.id)]
        except KeyError:
            filtering[str(ctx.guild.id)] = (1, 1)
        if int(value) and int('-1') < int(value) < 5 or int(value) == 0:
            filtering[str(ctx.guild.id)] = ((filtering[str(ctx.guild.id)])[0], int(value))
        else:
            raise ValueError('Invalid value for "content_check".')
        await ctx.send(f'Content filter level has been set to {value}.')


    @commands.command(aliases=('rm_swear', 'delete_swear', 'remove_swear'), description='Removes swear from current mode.')
    @commands.has_permissions(moderate_members=True)
    async def del_swear(self, ctx, *, string: str):
        if content == 0:
            await ctx.message.delete()
            raise IndexError(f"Explicit data check is currently disabled.")
        elif content == 1:
            if string in explicit_data2:
                explicit_data2.remove(string)
            else:
                await ctx.message.delete()
                raise IndexError(
                    f"Explicit_data2 does not contain {string} as a value.")
        elif content == 2:
            if string in explicit_data3:
                explicit_data3.remove(string)
            else:
                await ctx.message.delete()
                raise IndexError(
                    f"Explicit_data3 does not contain {string} as a value.")
        elif content == 3:
            if string in explicit_data4:
                explicit_data4.remove(string)
            else:
                await ctx.message.delete()
                raise IndexError(
                    f"Explicit_data4 does not contain {string} as a value.")
        elif content == 4:
            if string in explicit_data5:
                explicit_data5.remove(string)
            else:
                await ctx.message.delete()
                raise IndexError(
                    f"Explicit_data5 does not contain {string} as a value.")
        await ctx.send(f"{ctx.author.mention} swear was removed from the filter.")
        await ctx.message.delete()


    @commands.command(aliases=['append_swear'], description='Adds word for swear detection.')
    @commands.has_permissions(moderate_members=True)
    async def add_swear(self, ctx, *, string: str):
        if content == 0:
            await ctx.message.delete()
            raise IndexError(f"Explicit data check is currently disabled.")
            return
        elif content == 1:
            explicit_data2.add(string)
        elif content == 2:
            explicit_data3.add(string)
        elif content == 3:
            explicit_data4.add(string)
        elif content == 4:
            explicit_data5.add(string)
        await ctx.send(f'{ctx.author.mention}, swear was added to the filter.')
        await ctx.message.delete()


    @commands.command(aliases=['append_enhanced_swears'], description='Enhances swear detection for words in list.')
    @commands.has_permissions(moderate_members=True)
    async def add_enhanced_swears(self, ctx, *, swears):
        try:
            list(swears)
        except ValueError:
            raise ValueError('Invalid list for "swears"')
        test = []
        set = convert_to_list(swears)
        print(set)
        for i in set:
            for index, value in enumerate(str(i).replace(' ', '')):
                if ' ' in i:
                    dat = Functions.str_to_list(
                        Functions.list_to_str(Functions.spliceOutWords(str(i))))
                    dat[index] = '*'
                    test.insert(0, Functions.list_to_str(dat))
                    test.insert(0, i)
                else:
                    dat = Functions.str_to_list(str(i))
                    dat[index] = '*'
                    test.insert(0, Functions.list_to_str(dat))
                    test.insert(0, i)
                if content == 0:
                    await ctx.message.delete()
                    raise IndexError(f"Explicit data check is currently disabled.")
                    return
                elif content == 1:
                    explicit_data2.add(Functions.list_to_str(dat))
                    explicit_data2.add(i)
                elif content == 2:
                    explicit_data3.add(Functions.list_to_str(dat))
                    explicit_data3.add(i)
                elif content == 3:
                    explicit_data5.add(Functions.list_to_str(dat))
                    explicit_data5.add(i)
                elif content == 4:
                    explicit_data5.add(Functions.list_to_str(dat))
                    explicit_data5.add(i)
        await ctx.send(f'{ctx.author.mention}, swears was added to the filter.')
        await ctx.message.delete()


    @commands.command(aliases=['append_extra_enhanced_swears'], description='Ridiculously enhances swear detection for words in list.')
    @commands.has_permissions(moderate_members=True)
    async def add_extra_enhanced_swears(self, ctx, *, swears):
        try:
            list(swears)
        except ValueError:
            raise ValueError('Invalid list for "swears"')
        test = []
        set = convert_to_list(swears)
        print(set)
        cache = []
        list = []
        set = {}
        for i in set:
            for index, value in enumerate(str(i).replace(' ', '')):
                if ' ' in i:
                    dat = Functions.str_to_list(
                        Functions.list_to_str(Functions.spliceOutWords(str(i))))
                    dat[index] = '*'
                    list.append(Functions.list_to_str(dat))
                    list.append(i)
                else:
                    dat = Functions.str_to_list(str(i))
                    dat[index] = '*'
                    list.append(Functions.list_to_str(dat))
                    list.append(i)
                cache = Functions.list_to_str(dat)
                moveable_cache = Functions.str_to_list(cache)
                for char in (len(i) ** 2) * 'r':
                    moveable_cache[random.randint(0, len(i) - 1)] = '*'
                    if check(moveable_cache):
                        list.append(Functions.list_to_str(moveable_cache))
                    else:
                        continue
                    if content == 0:
                        await ctx.send('Explicit data check is currently disabled.')
                    elif content == 1:
                        explicit_data2.add(Functions.list_to_str(dat))
                        explicit_data2.add(i)
                        explicit_data2.add(Functions.list_to_str(moveable_cache))
                    elif content == 2:
                        explicit_data3.add(Functions.list_to_str(dat))
                        explicit_data3.add(i)
                        explicit_data3.add(Functions.list_to_str(moveable_cache))
                    elif content == 3:
                        explicit_data4.add(Functions.list_to_str(dat))
                        explicit_data4.add(i)
                        explicit_data4.add(Functions.list_to_str(moveable_cache))
                    elif content == 4:
                        explicit_data5.add(Functions.list_to_str(dat))
                        explicit_data5.add(i)
                        explicit_data5.add(Functions.list_to_str(moveable_cache))
        await ctx.send(f'{ctx.author.mention}, swears was added to the filter.')
        await ctx.message.delete()
  
  
@bot.command(aliases=('call', 'request'), description='Returns bot latency.')
async def ping(ctx):
    embed = discord.Embed(title='Status')
    if bot.latency * 1000 > 119:
        embed.color = discord.Color.from_rgb(0,255,0)
    elif bot.latency * 1000 > 79:
        embed.color = discord.Color.from_rgb(255,249,8)
    elif bot.latency * 1000 > 39:
        embed.color = discord.Color.from_rgb(141,255,8)
    else:
        embed.color = discord.Color.from_rgb(000, 255, 000)
    embed.add_field(name='Ping', value=str(round(bot.latency * 1000)) + ' ms.')
    embed.add_field(name='Ratelimited', value=f'{bot.is_ws_ratelimited()}')
    try:
        await bot.fetch_user(bot.user.id)
    except BaseException:
        embed.add_field(name='Connection', value='Down')
    else:
        embed.add_field(name='Connection', value='Working')
    async with ctx.message.channel.typing():
        try:
            await bot.wait_for(event='socket_event_type', timeout=10)
        except asyncio.exceptions.TimeoutError:
            embed.add_field(name='Websocket', value='Not recieving')
        else:
            embed.add_field(name='Websocket', value='Recieving')

        await asyncio.sleep(2)
    if success['last']:
        embed.add_field(name='Background ping', value=f'Last ping: Successful\nSuccessful pings: **{(success[True] / (success[True] + success[False])) * 100}%**')
    else:
        embed.add_field(name='Background ping', value=f'Last ping: Unsuccessful\nSuccessful pings: **{(success[True] / (success[True] + success[False])) * 100}%**')
    await ctx.message.reply(embed=embed)
  

@tasks.loop(minutes=1)
async def ping():
  try:
    await bot.fetch_user(bot.user.id)
  except BaseException:
    print('Connection to API terminated.')

ping.start()
  
bot.add_cog(cog=filtering(bot), override=True)

bot.run(TOKEN)
