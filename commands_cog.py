import discord
import random
import re
from discord.ext import commands
from config import DATA, save_data


class CommandsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    #set command to change urls and messages
    @commands.command(description='change the apply url, connection url and welcome message of the concierge', rest_is_raw=True)
    async def set(self, ctx, arg, *,text):
        """Admin: Change the apply url, connection url or the Welcome message. usage ~set <applyUrl|connectUrl|joinMessage> <text>. """
        
        set_command_dict = {"applyurl":"applyUrl","connecturl":"connectUrl", "joinmessage":"joinMessage"  }
        
        if not self.client.is_allowed(ctx):
            return

        arg = set_command_dict.get(arg.lower(), None)        
        if arg is not None and text is not None:
            DATA[arg] = text.strip()
            save_data()
            await ctx.send("Saved!")
        else:
            await ctx.send(" ~set argument is not valid. usage ~set <applyUrl|connectUrl|joinMessage> <text>.")
    
    

    #status command
    @commands.command(description='Get info about one or all the Minecraft servers')
    async def status(self, ctx, arg=None):
        """Get info about one or all the Minecraft servers"""
        channel = ctx.get_channel
        if not self.client.is_allowed(ctx):
            return

        if arg is not None:
            #get arg(server) info details a send that
            await ctx.send(arg+' info: blah blah blah')
        else:
            #send complete server list info
            await ctx.send('list of sever info')

    #howto command
    @commands.command(description='Get URL to connection intructions')
    async def howto(self, ctx):
        """Get URL to connection intructions"""
        author = ctx.message.author
        channel = await author.create_dm()
        await channel.send(DATA["connectUrl"])
        

    #roll command
    @commands.command(description='Roll a dice of your choice.')
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)
    
    #ban command
    @commands.command(description='ban a user from the minecraft servers')
    async def ban(self, ctx, ign: str):
        """Admin: ban a user from the minecraft servers."""
        if not self.client.is_allowed(ctx):
            return
        await ctx.send('Deploying ban hammer!')
    
    #schedule
    @commands.command(description='list the server reboot schedules')
    async def schedule(self, ctx):
        """list the server reboot schedules"""
        message = "Server reboot schedule \n"
        for line in self.client.schedule():
            message += "{server} : {time} \n".format(server=line[0], time=line[1])
        await ctx.send(message)