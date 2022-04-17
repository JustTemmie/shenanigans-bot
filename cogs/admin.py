import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, CheckFailure, command, has_permissions, bot_has_permissions




class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @command(name="kick", brief="Kicks the specified users")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets: Greedy[Member], *, reason:Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("One or more of the required arguments are missing")
            
        else:
            for target in targets:
                await target.kick(reason=reason)
                embed = Embed(title="Member kicked",
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                fields = [("Member", f"{target.mention} a.k.a. {target.display_name}", False),
                          ("Actioned by", ctx.author.mention, False),
                          ("ID", target.id, False),
                          ("Name", str(target), False),
                          ("Created at in UTC", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                          ("Joined at in UTC", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                          ("Top role", target.top_role.mention, False),
                          ("Reason", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                              
                embed.set_thumbnail(url=target.avatar_url)
                await self.bot.get_channel(772591539423281172).send(embed=embed)
                await ctx.send(embed=embed)
    
    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform tat task")

    
    @command(name="ban", brief="Bans the specified users")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, targets: Greedy[Member], *, reason:Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("One or more of the required arguments are missing")

        else:
            for target in targets:
                await target.ban(reason=reason)
                    
                embed = Embed(title="Member banned",
                              colour=0xDD2222,
                              timestamp=datetime.utcnow())

                fields = [("Member", f"{target.mention} a.k.a. {target.display_name}", False),
                          ("Actioned by", ctx.author.mention, False),
                          ("ID", target.id, False),
                          ("Name", str(target), False),
                          ("Created at in UTC", target.created_at.strftime(
                              "%d/%m/%Y %H:%M:%S"), True),
                          ("Joined at in UTC", target.joined_at.strftime(
                              "%d/%m/%Y %H:%M:%S"), True),
                          ("Top role", target.top_role.mention, False),
                          ("Reason", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                    
            embed.set_thumbnail(url=target.avatar_url)
            await self.bot.get_channel(772591539423281172).send(embed=embed)
            await ctx.send(embed=embed)

    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform tat task")
            
    
    @commands.command(name="clear", aliases=["purge"], brief="Clears messages equal to the amount specified ")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount = 0, shut = "shutupplz"):
        if amount >= 100:
            amount = 99
        if amount == 0:
            await ctx.send("please specifiy an amount")
            return
        if 0 < amount:
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=amount + 1):
                      messages.append(message)

            await channel.delete_messages(messages)
            if shut == "shutupplz":
                await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}', delete_after=10)
            else:
                pass

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")
    
    @commands.command(name="react")
    @has_permissions(manage_messages=True)
    async def react(self, ctx, msgid, reaction):
        if msgid == None or reaction == None:
            await ctx.send("Give me both a message and a reaction to react with")
        
        else:
            emoji = reaction
            message = await ctx.fetch_message(msgid)
            await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(admin(bot))