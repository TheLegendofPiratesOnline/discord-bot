# Filename: Commands.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

import discord
from discord.ext import commands

from bot.language import BotLocalizer
from bot.core import BotGlobals

from datetime import datetime

class Commands:
    """
    The Commands class will house all commands provided by the
    TLOPO Discord Bot.

    This will hopefully make it easier for any developers to add
    further commands to this bot.
    """

    def __init__(self):
        # TODO: Rewrite to be cleaner.

        @self.bot.command()
        async def oceans(ctx):

            """
            Returns server populations.
            """

            system_status = self.taskMgr.getSystemStatus()

            if system_status.get('status', 0) == 3:
                embed = BotLocalizer.MSG_CLOSED_SERVERS("Ocean population data is unavailable")

            else:
                oceans = self.taskMgr.getOceanPopulations()
                total = 0

                embed = discord.Embed(title="**Ocean Populations**", color=0x0066ff)

                for i, k in sorted(oceans.items()):
                    embed.add_field(name=i, value=k, inline=False)
                    total += k


                embed.add_field(name="Total", value="**%s**" % total, inline=False)
                
            # Response.
            await ctx.send(embed=embed)

        @self.bot.command()
        async def fleets(ctx):

            """
            Returns active fleets.
            """

            system_status = self.taskMgr.getSystemStatus()
            fleets = self.taskMgr.getActiveFleets()
            activeFleetCount = 0
            
            if system_status.get('status', 0) == 3:
                embed = BotLocalizer.MSG_CLOSED_SERVERS("Fleet data is unavailable")

            elif fleets:
                embed = discord.Embed(title="**Active Fleets**", color=0x0066ff)

                for i, k in sorted(fleets.items()):
                    if k.get('type') == '':
                        embed.add_field(name="**%s**" % i, value="No active fleet", inline=False)
                        activeFleetCount += 1
                    else:
                        embed.add_field(
                            name='**%s**' % i,
                            value=BotLocalizer.FLEET_ITEM_INFO % (
                                k.get('type'),
                                k.get('state'),
                                k.get('shipsRemaining')
                            ),
                            inline=False
                        )

                if activeFleetCount == len(fleets.items()):
                    embed = discord.Embed(title="**No active fleets**", color=0x0066ff)


            # Response.
            await ctx.send(embed=embed)

        @self.bot.command()
        async def invasions(ctx):

            """
            Returns active invasions.
            """

            invasions = self.taskMgr.getActiveInvasions()
            system_status = self.taskMgr.getSystemStatus()
            activeInvasionCount = 0

            if system_status.get('status', 0) == 3:
                embed = BotLocalizer.MSG_CLOSED_SERVERS("Invasion data is unavailable")

            else:
                embed = discord.Embed(title="**Active Invasions**", color=0x0066ff)

                for i, k in sorted(invasions.items()):
                    if k.get('state') == '':
                        embed.add_field(name='**%s**' % i, value="No active invasion", inline=False)
                        activeInvasionCount += 1
                    else:
                        embed.add_field(
                            name='**%s**' % i,
                            value=BotLocalizer.INVASION_ITEM_INFO % (
                                k.get('state'),
                                k.get('phase'),
                                k.get('numPlayers')
                            ),
                            inline=False
                        )

                if activeInvasionCount == len(invasions.items()):
                    embed = discord.Embed(title="**No active invasions**", color=0x0066ff)

            # Response.
            await ctx.send(embed=embed)

        @self.bot.command()
        async def notices(ctx):
            """
            Returns any server notices.
            """

            system_status = self.taskMgr.getSystemStatus()
            
            if system_status:
                notices = system_status.get('notices')
                status = BotGlobals.GLOB_CODE_TO_STATUS.get(int(system_status.get('status')), 'Unknown')
                outages = system_status.get('outages')

                embed = discord.Embed(title="**Server Notices**", color=0x0066ff)

                if notices:
                    tmp = ""
                    for i in notices.keys():
                        notice = notices[i]
                        msg = notice.get('text')

                        flag = BotGlobals.SRV_CODE_TO_STATUS.get(int(notice.get('flag')))
                        tmp += "\n**%s** | %s\n**Message:** *%s*\n" % (flag, i, msg)
                elif system_status.get('status', 0) == 3:
                    embed = BotLocalizer.MSG_CLOSED_SERVERS("Visit https://tlopo.com/ for more information.")
                else:
                    tmp = "No known notices."

                if system_status.get('status', 0) != 3:
                    embed.add_field(name=BotLocalizer.OVER_ALL_STATUS % status, value=BotLocalizer.SYSTEM_STATUS_INFO % (tmp, outages), inline=False)
                    embed.set_footer(text="*Status of prod-gs-1.tlopo.com is being detected incorrectly. This is an issue with the API.*")
            else:
                embed = discord.Embed(title="Server Notices Unavailable", color=0xff0000)

            await ctx.send(embed=embed)

        @self.bot.command()
        async def status(ctx):

            '''
            Returns current server status.
            '''

            system_status = self.taskMgr.getSystemStatus()

            if not system_status:
                await ctx.send(embed=discord.Embed(title="Server Status Unavailable", color=0xff0000))
                return

            if system_status.get('status', 0) == 3:
                await ctx.send(embed=BotLocalizer.MSG_CLOSED_SERVERS("Visit https://tlopo.com/ for more information."))
                return

            servers = system_status.get('servers') or {}
            webs = servers.get('web', [])
            cas = servers.get('client_agents', [])
            ais = servers.get('oceans', [])
            uds = servers.get('gameserver_functions', [])

            embed = discord.Embed(title="**Server Status**", color=0x0066ff)

            tmp = ""
            for server in webs:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Web Servers**", value=tmp, inline=False)

            tmp = ""
            for server in cas:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Client Agents**", value=tmp, inline=False)

            tmp = ""
            for server in ais:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Oceans**", value=tmp, inline=False)

            tmp = ""
            for server in uds:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Gameserver Functions**", value=tmp, inline=False)

            embed.set_footer(text="Status of prod-gs-1.tlopo.com is being detected incorrectly.\nThis is an issue with the TLOPO API.")

            await ctx.send(embed=embed)
        
        @self.bot.command()
        async def fullstatus(ctx):

            '''
            Returns current server status with more details.
            '''

            system_status = self.taskMgr.getSystemStatus()

            if not system_status:
                await ctx.send(embed=discord.Embed(title="Server Status Unavailable", color=0xff0000))
                return

            if system_status.get('status', 0) == 3:
                await ctx.send(embed=BotLocalizer.MSG_CLOSED_SERVERS("Visit https://tlopo.com/ for more information."))
                return

            servers = system_status.get('servers') or {}
            webs = servers.get('web', [])
            cas = servers.get('client_agents', [])
            ais = servers.get('oceans', [])
            uds = servers.get('gameserver_functions', [])

            embed = discord.Embed(title="**Server Status**", color=0x0066ff)

            tmp = ""
            for server in webs:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Web Servers**", value=tmp, inline=False)

            tmp = ""
            for server in cas:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Client Agents**", value=tmp, inline=False)

            tmp = ""
            for server in ais:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Oceans**", value=tmp, inline=False)

            tmp = ""
            for server in uds:
                flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                tmp += "**%s**:  %s\n" % (server.get('name', 'Unknown'), flag)
            embed.add_field(name="**Gameserver Functions**", value=tmp, inline=False)

            embed.set_footer(text="Status of prod-gs-1.tlopo.com is being detected incorrectly.\nThis is an issue with the TLOPO API.")

            await ctx.send(embed=embed)
