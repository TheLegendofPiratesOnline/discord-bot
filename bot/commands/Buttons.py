import discord
from discord.ext import commands

from bot.language import BotLocalizer, BotTranslate
from bot.core import BotGlobals, BotCore

from datetime import datetime

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
        # Create base embed with article info
        embed = discord.Embed(
            title=BotGlobals.FORMAT_STRINGS.get('bold') % self.news[self.article_number].get('title'),
            description=self.news[self.article_number].get('summary'),
            url=self.news[self.article_number].get('url'),
            color=BotGlobals.EMBED_COLOR.get('news'),
            type='rich'
        )

        # Set author image based on author name
        if self.news[self.article_number].get('author') == "The Crew":
            auther_img = 'https://tlopo.com/static/img/PiratesWebsiteLogoSmall.png'
        else:
            auther_img = None

        # Set embed author and image
        discord.Embed.set_author(
            embed,
            name=self.news[self.article_number].get('author'),
            icon_url=auther_img
        )
        discord.Embed.set_image(embed, url=self.news[self.article_number].get('picurl'))
        
        # Create footer info with article date and pagination
        footer_info = "%s\n[%s/%s]" % (self.news[self.article_number].get('date'), self.article_number + 1, len(self.news))

        # Add translation warning if using auto-translate
        if BotLocalizer.AUTOTRANSLATE_IN_USE:
            discord.Embed.set_footer(
                embed,
                text= "%s\n%s" % (footer_info, BotLocalizer.AUTO_TRANSLATE_WARNING)
            )
        else:
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

class ReleaseButtons(discord.ui.View):
    def __init__(self, releases: list = None, release_number: int = 0):
        super().__init__()
        self.release_number = release_number
        self.releases = releases

    def create_release_embed(self) -> discord.Embed:
        """
        Create a release embed for the given release number.

        returns:
            discord.Embed: The embed for the release notes.
            
        """
        # Get current release data
        release = self.releases[self.release_number]
        
        # Create base embed
        embed = discord.Embed(
            title=BotGlobals.FORMAT_STRINGS.get('bold') % release.get('version', 'Unknown Version'),
            description=release.get('date', 'Unknown Date'),
            url=release.get('url', ''),
            color=BotGlobals.EMBED_COLOR.get('news'),
            type='rich'
        )

        sections = release.get('sections', {})
        
        # Process each section
        for section_name, items in sections.items():
            if not items:
                continue
                
            formatted_items = []
            
            # Format each item and its sub-items
            for item in items:
                text = BotGlobals.FORMAT_STRINGS.get('release_text') % item.get('text', '')
                
                sub_items_text = ''
                
                # Add sub-items if any
                sub_items = item.get('sub_items', [])
                for sub_item in sub_items:
                    sub_items_text += BotGlobals.FORMAT_STRINGS.get('release_sub_text') % sub_item
                    
                formatted_items.append(text + sub_items_text)
            
            section_text = '\n'.join(formatted_items)
            
            # Handle long sections (Discord has 1024 character limit)
            if len(section_text) > 1024:
                chunks = []
                current_chunk = []
                current_length = 0
                
                # Split content into chunks
                for item in formatted_items:
                    if current_length + len(item) + 1 > 1000:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = [item]
                        current_length = len(item)
                    else:
                        current_chunk.append(item)
                        current_length += len(item) + 1
                
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                
                # Add each chunk as a separate field
                for i, chunk in enumerate(chunks):
                    if len(embed.fields) < 25:  # Discord's field limit
                        field_name = BotGlobals.FORMAT_STRINGS.get('bold') % section_name
                        if i > 0:
                            field_name += " (continued %d)" % (i + 1)
                        
                        embed.add_field(
                            name=field_name,
                            value=chunk if chunk else BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.RELEASE_STRINGS.get('no_items'),
                            inline=False
                        )
            else:
                # Add shorter sections as a single field
                if len(embed.fields) < 25:
                    embed.add_field(
                        name=BotGlobals.FORMAT_STRINGS.get('bold') % section_name,
                        value=section_text if section_text else BotGlobals.FORMAT_STRINGS.get('bold') % BotLocalizer.RELEASE_STRINGS.get('no_items'),
                        inline=False
                    )
        
        # Add pagination footer
        footer_info = "[%s/%s]" % (self.release_number + 1, len(self.releases))
        
        # Add translation warning if needed
        if BotLocalizer.AUTOTRANSLATE_IN_USE:
            discord.Embed.set_footer(
                embed,
                text="%s\n%s" % (footer_info, BotLocalizer.AUTO_TRANSLATE_WARNING)
            )
        else:
            discord.Embed.set_footer(
                embed,
                text=footer_info
            )
        
        return embed
    
    @discord.ui.button(label=BotLocalizer.RELEASE_STRINGS.get('previous_button'), style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Previous release button
        """
        if self.release_number > 0:
            self.release_number -= 1
            embed = self.create_release_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    
    @discord.ui.button(label=BotLocalizer.RELEASE_STRINGS.get('next_button'), style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Next release button
        """
        if self.release_number < len(self.releases) - 1:
            self.release_number += 1
            embed = self.create_release_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
