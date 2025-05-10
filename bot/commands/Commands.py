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

from bot.language import BotLocalizer, BotTranslate
from bot.core import BotGlobals, BotCore
from bot.commands import Buttons

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
        #       Rewrite code to use / commands instead of outdated string commands. (maybe get rid of string commands completly?)


        @self.bot.command()
        async def help(ctx):
            """
            Returns a list of all commands.
            """

            embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[0], color=BotGlobals.EMBED_COLOR.get('help'))
            for command in self.bot.commands:
                name = command.name
                if command.help:
                    if BotLocalizer.AUTOTRANSLATE_IN_USE == True:

                        debug = 'help_translate' in BotGlobals.DEBUG_MODULES
                        translator = BotTranslate.BotTranslate(debug, BotCore.LANGUAGE)

                        desc = translator.translate_string(command.help)

                        if debug:
                            print('[DEBUG] Translated help string: %s' % desc)

                        embed.set_footer(
                            text= BotLocalizer.AUTO_TRANSLATE_WARNING
                        )
                    else:
                        desc = command.help
                else:
                    desc = BotLocalizer.STATUS_MESSAGES[0]
                usage = "%s%s" % (ctx.prefix, name)  # Overcomplicating this incase a non string command is added in the future.

                # Add field for each command
                discord.Embed.add_field(
                    embed,
                    name= BotGlobals.FORMAT_STRINGS.get('bold') % usage,
                    value=desc,
                    inline=False
                )

            await ctx.send(embed=embed)

        @self.bot.command()
        async def about(ctx):
            """
            Returns information about bot.
            """

            embed = discord.Embed(
                title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[1],
                description= BotLocalizer.APP_DESCRIPTION,
                color=BotGlobals.EMBED_COLOR.get('about'))
            
            try:
                with open(BotGlobals.AUTHORS_FILENAME, 'r') as f:
                    authors = f.read()

                    if authors == "":
                        authors = BotLocalizer.STATUS_MESSAGES[1]

            except FileNotFoundError:
                authors = BotLocalizer.STATUS_MESSAGES[1]
            
            discord.Embed.add_field(
                embed,
                name=BotLocalizer.FIELD_NAMES[0],
                value=authors,
                inline=False
            )

            if self.settings.getSetting('showLink') == True:
                discord.Embed.add_field(
                    embed,
                    name=BotLocalizer.STATUS_MESSAGES[12],
                    value=self.settings.getSetting('link'),
                    inline=False
                )
            else:
                discord.Embed.add_field(
                    embed,
                    name=BotLocalizer.STATUS_MESSAGES[12],
                    value=BotLocalizer.STATUS_MESSAGES[0],
                    inline=False
                )

            if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                discord.Embed.set_footer(
                    embed,
                    text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                )

            await ctx.send(embed=embed)

        @self.bot.command()
        async def oceans(ctx):

            """
            Returns server populations.
            """

            system_status = self.taskMgr.getSystemStatus()

            if system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )

            else:
                oceans = self.taskMgr.getOceanPopulations()
                total = 0

                embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[2], color=BotGlobals.EMBED_COLOR.get('oceans'))

                # Loop through each ocean and add it to the embed.
                for i, k in sorted(oceans.items()):
                    discord.Embed.add_field(
                        embed,
                        name=i,
                        value=k,
                        inline=False
                    )
                    total += k

                # Add total population to the embed.
                discord.Embed.add_field(
                    embed,
                    name=BotLocalizer.FIELD_NAMES[1],
                    value=BotGlobals.FORMAT_STRINGS.get('bold') % total,
                    inline=False
                )

            if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                discord.Embed.set_footer(
                    embed,
                    text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                )
                
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
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )

            elif fleets:
                embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[3], color=BotGlobals.EMBED_COLOR.get('fleets'))

                # Loop through each fleet and add it to the embed.
                for i, k in sorted(fleets.items()):
                    if k.get('type') == '':
                        discord.Embed.add_field(
                            embed,
                            name=BotGlobals.FORMAT_STRINGS.get('bold') % i,
                            value=BotLocalizer.STATUS_MESSAGES[2],
                            inline=False
                        )
                        activeFleetCount += 1

                    else:
                        discord.Embed.add_field(
                            embed,
                            name=BotGlobals.FORMAT_STRINGS.get('bold') % i,
                            value=BotLocalizer.FLEET_ITEM_INFO % (
                                k.get('type'),
                                k.get('state'),
                                k.get('shipsRemaining')
                            ),
                            inline=False
                        )

                if activeFleetCount != len(fleets.items()):
                    embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[4], color=BotGlobals.EMBED_COLOR.get('fleets'))

            if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                discord.Embed.set_footer(
                    embed,
                    text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                )

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
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )

            else:
                embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[5], color=BotGlobals.EMBED_COLOR.get('invasions'))
                
                # Loop through each invasion and add it to the embed.
                for i, k in sorted(invasions.items()):
                    if k.get('state') == '':
                        discord.Embed.add_field(
                            embed,
                            name=BotGlobals.FORMAT_STRINGS.get('bold') % i,
                            value = BotLocalizer.STATUS_MESSAGES[3],
                            inline=False
                        )
                        activeInvasionCount += 1
                    else:
                        discord.Embed.add_field(
                            embed,
                            name=BotGlobals.FORMAT_STRINGS.get('bold') % i,
                            value=BotLocalizer.INVASION_ITEM_INFO % (
                                k.get('state'),
                                k.get('phase'),
                                k.get('numPlayers')
                            ),
                            inline=False
                        )

                if activeInvasionCount == len(invasions.items()):
                    embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[6], color=BotGlobals.EMBED_COLOR.get('invasions'))

            if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                discord.Embed.set_footer(
                    embed,
                    text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                )

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
                status = BotLocalizer.GLOB_CODE_TO_STATUS.get(int(system_status.get('status')), BotLocalizer.STATUS_MESSAGES[10])
                outages = system_status.get('outages')

                embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[7], color=BotGlobals.EMBED_COLOR.get('notices'))

                if notices:
                    tmp = ""
                    for i in notices.keys():
                        notice = notices[i]
                        msg = notice.get('text')
                        flag = BotLocalizer.SRV_CODE_TO_STATUS.get(int(notice.get('flag')))
                        tmp += BotGlobals.FORMAT_STRINGS.get('notice_format') % (flag, BotLocalizer.MISC[0], i, msg)

                elif system_status.get('status', 0) == 3:
                    embed = discord.Embed(
                        title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[12],
                        description=BotLocalizer.STATUS_MESSAGES[8],
                        color=BotGlobals.EMBED_COLOR.get('offline')
                    )
                    return
                
                else:
                    tmp = BotLocalizer.STATUS_MESSAGES[4]

                discord.Embed.add_field(
                    embed,
                    name=BotLocalizer.OVER_ALL_STATUS % status,
                    value=BotLocalizer.SYSTEM_STATUS_INFO % (tmp, outages),
                    inline=False
                )
                
                # Autotranslate warning.
                # User warning that api isnt reading prod-gs-1.tlopo.com correctly. Remove when fixed.
                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= "%s\n%s" % (BotLocalizer.STATUS_MESSAGES[9], BotLocalizer.AUTO_TRANSLATE_WARNING)
                    )
                else:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.STATUS_MESSAGES[9]
                    )

            else:
                embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[10], color=BotGlobals.EMBED_COLOR.get('error'))

                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                    )

            await ctx.send(embed=embed)

        @self.bot.command()
        async def status(ctx):

            """
            Returns current server status.
            """

            system_status = self.taskMgr.getSystemStatus()
            servers = system_status.get('servers')
            webs = servers.get('web', [])
            cas = servers.get('client_agents', [])
            ais = servers.get('oceans', [])
            uds = servers.get('gameserver_functions', [])

            embed = discord.Embed(title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[8], color=BotGlobals.EMBED_COLOR.get('status'))

            if system_status:
                # Loop through each server and add it to the embed.

                # Add web server status to the embed.
                tmp = ""
                for server in webs:
                    flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[2],
                    value=tmp,
                    inline=False
                )

                # Add client agent status to the embed.
                tmp = ""
                for server in cas:
                    flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[3],
                    value=tmp,
                    inline=False
                )

                # Add ocean status to the embed.
                tmp = ""
                for server in ais:
                    flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[4],
                    value=tmp,
                    inline=False
                )

                # Add gameserver functions status to the embed.
                tmp = ""
                for server in uds:
                    flag = BotGlobals.GLOB_CODE_TO_EMOJI.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[5],
                    value=tmp,
                    inline=False
                )

                # Autotranslate warning.
                # User warning that api isnt reading prod-gs-1.tlopo.com correctly. Remove when fixed.
                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= "%s\n%s" % (BotLocalizer.STATUS_MESSAGES[9], BotLocalizer.AUTO_TRANSLATE_WARNING)
                    )
                else:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.STATUS_MESSAGES[9]
                    )
            
            elif system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )

                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                    )

            else:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[9],
                    color=BotGlobals.EMBED_COLOR.get('error')
                )

                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                    )

            await ctx.send(embed=embed)
        
        @self.bot.command()
        async def fullstatus(ctx):

            """
            Returns current server status with more details.
            """

            system_status = self.taskMgr.getSystemStatus()
            servers = system_status.get('servers')
            webs = servers.get('web', [])
            cas = servers.get('client_agents', [])
            ais = servers.get('oceans', [])
            uds = servers.get('gameserver_functions', [])

            embed = discord.Embed(
                title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[8],
                color=BotGlobals.EMBED_COLOR.get('fullstatus')
            )

            if system_status:
                # Loop through each server and add it to the embed.

                # Add web server status to the embed.
                tmp = ""
                for server in webs:
                    flag = BotLocalizer.GLOB_CODE_TO_STATUS.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[2],
                    value=tmp,
                    inline=False
                )

                # Add client agent status to the embed.
                tmp = ""
                for server in cas:
                    flag = BotLocalizer.GLOB_CODE_TO_STATUS.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[3],
                    value=tmp,
                    inline=False
                )

                # Add ocean status to the embed.
                tmp = ""
                for server in ais:
                    flag = BotLocalizer.GLOB_CODE_TO_STATUS.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[4],
                    value=tmp,
                    inline=False
                )

                # Add gameserver functions status to the embed.
                tmp = ""
                for server in uds:
                    flag = BotLocalizer.GLOB_CODE_TO_STATUS.get(server.get('status', 0))
                    tmp += BotGlobals.FORMAT_STRINGS.get('server_status') % (server.get('name', BotLocalizer.STATUS_MESSAGES[10]), flag)
                discord.Embed.add_field(
                    embed,
                    name=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.FIELD_NAMES[5],
                    value=tmp,
                    inline=False
                )

                # Autotranslate warning.
                # User warning that api isnt reading prod-gs-1.tlopo.com correctly. Remove when fixed.
                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= "%s\n%s" % (BotLocalizer.STATUS_MESSAGES[9], BotLocalizer.AUTO_TRANSLATE_WARNING)
                    )
                else:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.STATUS_MESSAGES[9]
                    )
            
            elif system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )

                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                    )

            else:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[9],
                    color=BotGlobals.EMBED_COLOR.get('error')
                )

                if BotLocalizer.AUTOTRANSLATE_IN_USE == True:
                    discord.Embed.set_footer(
                        embed,
                        text= BotLocalizer.AUTO_TRANSLATE_WARNING,
                    )

            await ctx.send(embed=embed)

        @self.bot.command()
        async def news(ctx):
            """
            Returns latest news articles.
            """

            news = self.taskMgr.getNewsFeed()
            system_status = self.taskMgr.getSystemStatus()
            
            if system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )
                await ctx.send(embed=embed)
            
            else:
                view = Buttons.NewsButtons(news)

                embed = view.create_news_embed()

                await ctx.send(embed=embed, view=view)
        
        @self.bot.command()
        async def releases(ctx):
            """
            Returns latest releases.
            """

            releases = self.taskMgr.getReleaseFeed()
            system_status = self.taskMgr.getSystemStatus()
            
            if system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )
                await ctx.send(embed=embed)
            
            else:
                view = Buttons.ReleaseButtons(releases)

                embed = view.create_release_embed()

                await ctx.send(embed=embed, view=view)
    
        @self.bot.command()
        async def notification(ctx):
            """
            Returns the current news banner on the TLOPO website.
            """

            system_status = self.taskMgr.getSystemStatus()
            notification = self.taskMgr.getNewsNotifications()

            if system_status.get('status', 0) == 3:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[11],
                    description=BotLocalizer.STATUS_MESSAGES[8],
                    color=BotGlobals.EMBED_COLOR.get('offline')
                )
            elif notification:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % notification.get('title'),
                    description=notification.get('datetime'),
                    url=BotGlobals.TLOPO_URL,
                    color=BotGlobals.EMBED_COLOR.get('notices')
                )
            else:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.EMBED_TITLES[12],
                    url=BotGlobals.TLOPO_URL,
                    color=BotGlobals.EMBED_COLOR.get('status')
                )

            await ctx.send(embed=embed)