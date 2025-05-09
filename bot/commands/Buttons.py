import discord
from discord.ext import commands

from bot.language import BotLocalizer, BotTranslate
from bot.core import BotGlobals, BotCore

from datetime import datetime

# TODO: Add strings to BotLocalizer and BotLocalizerTranslationTemplate

class NewsButtons(discord.ui.View):
    def __init__(self, news: list = None, article_number: int = 0):
        super().__init__()
        self.article_number = article_number
        self.news = news

    def create_news_embed(self) -> discord.Embed:
            """
            Create a news embed for the given article number.

            returns:
                discord.Embed: The embed for the news article.
            """

            if BotLocalizer.AUTOTRANSLATE_IN_USE:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % self.news[self.article_number].get('title'),
                    description=self.news[self.article_number].get('summary'),
                    url=self.news[self.article_number].get('url'),
                    color=BotGlobals.EMBED_COLOR.get('news'),
                    type='rich'
                )

                if self.news[self.article_number].get('author') == "The Crew":
                    auther_img = 'https://tlopo.com/static/img/PiratesWebsiteLogoSmall.png'
                else:
                    auther_img = None

                discord.Embed.set_author(
                    embed,
                    name=self.news[self.article_number].get('author'),
                    icon_url=auther_img
                )
                discord.Embed.set_image(embed, url=self.news[self.article_number].get('picurl'))
                
                footer_info = "%s\n[%s/%s]" % (self.news[self.article_number].get('date'), self.article_number + 1, len(self.news))

                discord.Embed.set_footer(
                    embed,
                    text= "%s\n%s" % (footer_info, BotLocalizer.AUTO_TRANSLATE_WARNING)
                )

                return embed
            
            else:
                embed = discord.Embed(
                    title=BotGlobals.FORMAT_STRINGS.get('bold') % self.news[self.article_number].get('title'),
                    description=self.news[self.article_number].get('summary'),
                    url=self.news[self.article_number].get('url'),
                    color=BotGlobals.EMBED_COLOR.get('news'),
                    type='rich'
                )

                if self.news[self.article_number].get('author') == "The Crew":
                    auther_img = 'https://tlopo.com/static/img/PiratesWebsiteLogoSmall.png'
                else:
                    auther_img = None

                discord.Embed.set_author(
                    embed,
                    name=self.news[self.article_number].get('author'),
                    icon_url=auther_img
                )
                discord.Embed.set_image(embed, url=self.news[self.article_number].get('picurl'))
                
                footer_info = "%s\n[%s/%s]" % (self.news[self.article_number].get('date'), self.article_number + 1, len(self.news))

                discord.Embed.set_footer(
                    embed,
                    text= footer_info
                )

                return embed
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Previous article button
        """
        if self.article_number > 0:
            self.article_number -= 1
            embed = self.create_news_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Next article button
        """
        if self.article_number < len(self.news) - 1:
            self.article_number += 1
            embed = self.create_news_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
