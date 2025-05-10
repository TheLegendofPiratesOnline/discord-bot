# Filename: BotTasks.py
# Author: mfwass
# Date: January 8th, 2017
#
# The Legend of Pirates Online Software
# Copyright (c) The Legend of Pirates Online. All rights reserved.
#
# All use of this software is subject to the terms of the revised BSD
# license.  You should have received a copy of this license along
# with this source code in a file named "LICENSE."

from bot.core import BotGlobals
from bot.language import BotLocalizer, BotTranslate
import threading
import requests
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class BotTasks:
    """
    The BotTasks class will be responsible for
    keeping tabs on all looping tasks.
    """

    def __init__(self, maxNewsAricles: int=5, debug: bool=False, language: str='en', maxReleaseNotes: int=5):
        self.activeFleets = {}
        self.activeInvasions = {}
        self.oceanPopulations = {}
        self.systemStatus = {}
        self.newsFeed = []
        self.newsNotifications = {}
        self.releaseFeed = {}
        self.maxNewsAricles = maxNewsAricles
        self.debug = debug
        self.language = language
        self.maxReleaseNotes = maxReleaseNotes

    def initializeTasks(self, tasks):
        print(":BotTasks: Initializing tasks...")

        for task in tasks:
            getattr(self, task)(task, tasks.get(task))

    ## BOT TASKS
    """
    Example Task Function

    !!! Make sure you add any new tasks to BotGlobals!

    def task_example(self, name, task):
        # Required code to make the task repeat.
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()

        # Task code here.

    """

    def task_news_notification(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        resp = self.contactAPI(task.get('api_url'))
        newsNotifications = {}
        if resp:
            newsNotifications = {
                'message': resp.get('message'),
                'datetime': resp.get('datetime'),
            }
        
        self.setNewsNotifications(newsNotifications)


    def task_release_feed(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        releaseNotes = []
        
        try:
            if self.maxReleaseNotes > 10:   
                for i in range(0, self.maxReleaseNotes, 10):
                    resp = self.contactAPI(task.get('api_url') % (10, i))
                    if resp is None:
                        print("Warning: API request failed for offset %s" % i)
                        continue

                    for release_info in resp:
                        try:
                            release = self.get_release_notes(release_info.get('url'))
                            if release:  # Make sure we got valid data
                                release['date'] = release_info.get('date')
                                release['url'] = release_info.get('url')
                                releaseNotes.append(release)
                        except Exception as e:
                            print("Error processing release: %s" % str(e))

            else:
                resp = self.contactAPI(task.get('api_url') % (self.maxReleaseNotes, 0))
                
                if resp:
                    for release_info in resp:
                        try:
                            release = self.get_release_notes(release_info.get('url'))
                            if release:  # Make sure we got valid data
                                release['date'] = release_info.get('date')
                                release['url'] = release_info.get('url')  # Add URL (was missing)
                                releaseNotes.append(release)
                        except Exception as e:
                            print("Error processing release: %s" % str(e))
            
            # Always update the feed with whatever we got
            self.setReleaseFeed(releaseNotes)
            
            if self.debug and 'task_release_feed' in BotGlobals.DEBUG_MODULES:
                print(json.dumps(releaseNotes, indent=4) +"\n\nNum release notes: " + str(len(releaseNotes)))
        
        except Exception as e:
            print("Fatal error in task_release_feed: %s" % str(e))
            # Set empty feed in case of error
            self.setReleaseFeed([])


    def task_news_feed(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        if self.maxNewsAricles > 10:   
            news=[]

            for i in range(0, self.maxNewsAricles, 10):
                resp = self.contactAPI(task.get('api_url') % (10, i))

                for i in resp:
                    news_item = {
                        'url': i.get('url'),
                        'picurl': i.get('picurl'),
                        'title': i.get('title'),
                        'author': i.get('author'),
                        'date': i.get('date'),
                        'summary': i.get('summary')
                    }

                    news.append(news_item)

        else:
            resp = self.contactAPI(task.get('api_url') % (self.maxNewsAricles, 0))

            news=[]
            for i in resp:
                news_item = {
                    'id': i.get('id'),
                    'url': i.get('url'),
                    'picurl': i.get('picurl'),
                    'title': i.get('title'),
                    'author': i.get('author'),
                    'date': i.get('date'),
                    'summary': i.get('summary')
                }

                news.append(news_item)

        self.setNewsFeed(news)

        if self.debug and 'task_news_feed' in BotGlobals.DEBUG_MODULES:
            print(json.dumps(news, indent=4) +"\n\nNum articals: " + str(len(news)))   


    def task_system_status(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        resp = self.contactAPI(task.get('api_url'))
        if resp:
            servers = resp.get('servers')
            if servers:
                outages = [j.get('name', 'Error-NoName')
                           for i in servers.keys()
                           for j in servers.get(i)
                           if j.get('status') != BotLocalizer.STATUS_ALIVE_SRV]
            else:
                outages = []

            out = {}
            out['status'] = resp.get('status')
            out['notices'] = resp.get('notices', 0) or None
            out['outages'] = outages or None
            out['servers'] = resp.get('servers')
            self.setSystemStatus(out)

            if self.debug and 'task_system_status' in BotGlobals.DEBUG_MODULES:
                print(json.dumps(out, indent=4) +"\n\nNum outages: " + str(len(outages)))

    def task_shards(self, name, task):
        threading.Timer(task.get('time'), getattr(self, name), args=[name, task]).start()
        resp = self.contactAPI(task.get('api_url'))
        if resp:
            fleets = {}
            invasions = {}
            populations = {}

            for shardId in resp.keys():
                # Get the information on the ocean.
                shardInfo = resp.get(shardId)
                available = shardInfo.get('available')

                if not available:
                    # Don't check the information on an offline ocean.
                    continue

                fleet = shardInfo.get('fleet')
                invasion = shardInfo.get('invasion')
                name = shardInfo.get('name')

                # Assign active fleets/invasions.
                if fleet:
                    fleets[name] = fleet

                if invasion:
                    invasions[name] = invasion

                # Set the population of this shard.
                populations[name] = shardInfo.get('population')

            # Set active fleets.
            self.setActiveFleets(fleets)
            self.setActiveInvasions(invasions)
            self.setOceanPopulations(populations)

            if self.debug and 'task_shards' in BotGlobals.DEBUG_MODULES:
                if 'task_shards_fleets' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG][task_shards][fleets]')
                    print(json.dumps(fleets, indent=4) +"\n\nNum fleets: " + str(len(fleets)))
                if 'task_shards_invasions' in BotGlobals.DEBUG_MODULES:
                    print(json.dumps(invasions, indent=4) +"\n\nNum invasions: " + str(len(invasions)))
                if 'task_shards_populations' in BotGlobals.DEBUG_MODULES:
                    print(json.dumps(populations, indent=4) +"\n\nNum populations: " + str(len(populations)))

    ## Other task functions.
    def contactAPI(self, apiUrl):
        """
        Contacts API and return its response in JSON format.
        """

        r = requests.get(apiUrl)

        try:
            # Just in case the API url dies, it's sanity check this.
            r = json.loads(r.text)
        except:
            print(":BotTasks(error): Failed to contact API.")
            r = None

        return r
    
    def translate_news_feed(self, news: list) -> list:
        """
        Translate the news feed using the BotTranslate class.

        Args:
            news (list): The news feed to translate.

        Returns:
            list: The translated news feed.
        """


        translate=BotTranslate.BotTranslate(self.debug, self.language)
  
        translated_news=[]

        if self.debug and 'translate_news_feed' in BotGlobals.DEBUG_MODULES:
            print(json.dumps(news, indent=4) +"\n\nNum articals: " + str(len(news)))

        for i in news:

            translated_news_item = {
                'id': i.get('id'),
                'url': i.get('url'),
                'picurl': i.get('picurl'),
                'title': translate.translate_string(i.get('title')),
                'author': i.get('author'),
                'date': i.get('date'),
                'summary': translate.translate_string(i.get('summary'))
            }

            translated_news.append(translated_news_item)

            if self.debug and 'translate_news_feed' in BotGlobals.DEBUG_MODULES:
                print('[DEBUG][translated_news_feed] Added translated news item: %s' % translated_news_item)

        return translated_news
    
    def get_release_notes(self, url: str) -> dict:
        """
        Scrapes the release notes from the TLOPO website.

        Args:
            url (str): The URL to scrape for release notes.

        Returns:
            dict: The release notes data.
        """
        # Default structure for release data
        release_data = {
            'version': 'Unknown Version',
            'sections': {}
        }
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                try:
                    # Load the page
                    page.goto(url)
                    page.wait_for_timeout(3000)  # Wait for content to render
                    page_source = page.content()
                    
                    # Parse HTML
                    soup = BeautifulSoup(page_source, 'html.parser')
                    article_box = soup.find('article', class_='box center')
                    
                    if article_box:
                        # Get release metadata
                        date_span = article_box.find('span', class_='releasenotedate')
                        if date_span:
                            release_data['date'] = date_span.text.strip()

                        version_span = article_box.find('span', class_='releasenoteversion')
                        if version_span:
                            release_data['version'] = version_span.text.strip()
                        
                        # Get content
                        content_div = article_box.find('div', class_='releasenotecontent')
                        if content_div:
                            sections = {}
                            section_titles = content_div.find_all('h4', class_='title is-4')
                            
                            for title in section_titles:
                                section_name = title.text.strip()
                                if not section_name:
                                    continue
                                    
                                section_ul = title.find_next('ul')
                                if section_ul:
                                    items = []
                                    
                                    top_li_items = section_ul.find_all('li', class_='releasenotecontentitem', recursive=False)
                                    
                                    for li in top_li_items:
                                        item_text_parts = []
                                        for content in li.contents:
                                            if isinstance(content, str):
                                                item_text_parts.append(content.strip())
                                            elif content.name == 'ul':
                                                break
                                        
                                        item_text = ' '.join(filter(None, item_text_parts))
                                        
                                        if not item_text:
                                            item_text = li.get_text(strip=True)
                                        
                                        # Get sub-items
                                        sub_items = []
                                        next_element = li.find_next_sibling()
                                        if next_element and next_element.name == 'ul':
                                            for sub_li in next_element.find_all('li', class_='releasenotecontentitem'):
                                                sub_text = sub_li.get_text(strip=True)
                                                sub_items.append(sub_text)
                                        
                                        item_text = item_text.strip()
                                        
                                        items.append({
                                            "text": item_text,
                                            "sub_items": sub_items
                                        })
                                    
                                    sections[section_name] = items
                            
                            release_data['sections'] = sections

                            if self.debug and 'get_release_notes_items' in BotGlobals.DEBUG_MODULES:
                                print('[DEBUG][get_release_notes_items] Added release notes items: \n%s' % json.dumps(release_data, indent=4))
                    
                except Exception as e:
                    print("Error scraping release notes: %s" % str(e))
                
                finally:
                    browser.close()
            
            return release_data
            
        except Exception as e:
            print("Fatal error in get_release_notes: %s" % str(e))
            return release_data  # Return the default structure in case of error
    
    def translate_release_notes(self, release: list) -> list:
        """
        Translate the release notes using the BotTranslate class.

        Args:
            release (list): The release notes to translate.

        Returns:
            list: The translated release notes.
        """
        if not release:  # Check if list is empty
            return []
            
        translate = BotTranslate.BotTranslate(self.debug, self.language)
        translated_release = []

        try:
            for i in release:
                    
                translated_release_item = {
                    'version': i.get('version', 'Unknown Version'),
                    'date': i.get('date', ''),
                    'url': i.get('url', ''),
                    'sections': {}
                }

                sections = i.get('sections', {})
                for section_name, items in sections.items():
                    translated_items = []
                    for item in items:
                            
                        text = translate.translate_string(item.get('text', ''))
                        sub_items = []
                        for sub_item in item.get('sub_items', []):
                            sub_items.append(translate.translate_string(sub_item))
                        
                        translated_items.append({
                            'text': text,
                            'sub_items': sub_items
                        })
                        
                    translated_release_item['sections'][section_name] = translated_items

                translated_release.append(translated_release_item)
                if self.debug and 'translated_release_item' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG][translated_release_item] Added translated news item: %s' % translated_release_item)

            if self.debug and 'translated_release' in BotGlobals.DEBUG_MODULES:
                print('[DEBUG][translated_release] Added translated release: %s' % translated_release)

            return translated_release
        except Exception as e:
            print("Error translating release notes: %s" % str(e))
            return release  # Return original if translation fails
    
    def translate_news_notifications(self, notification: list|None) -> list|None:
        """
        Translate the news notifications using the BotTranslate class.

        Args:
            news (list): The news notifications to translate.

        Returns:
            list: The translated news notifications.
        """

        if notification: 
            translate = BotTranslate.BotTranslate(self.debug, self.language)
            translated_notification = {
                'message': translate.translate_string(notification.get('message')),
                'datetime': notification.get('datetime')
            }

            if self.debug and 'translated_news_notifications' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG][translate_news_notifications] Added translated news item: %s' % translated_notification.get('message'))

            return translated_notification
        else:
            if self.debug and 'translated_news_notifications' in BotGlobals.DEBUG_MODULES:
                    print('[DEBUG][translate_news_notifications] No news notifications to translate.')

            return None

    def setActiveFleets(self, fleets):
        """
        Set active fleets.
        """

        self.activeFleets = fleets

    def getActiveFleets(self):
        """
        Get active fleets.
        """

        return self.activeFleets

    def setSystemStatus(self, status):
        """
        Set system status.
        """

        self.systemStatus = status

    def getSystemStatus(self):
        """
        Get system status.
        """

        return self.systemStatus

    def setActiveInvasions(self, invasions):
        """
        Set active invasions.
        """

        self.activeInvasions = invasions

    def getActiveInvasions(self):
        """
        Get active invasions.
        """

        return self.activeInvasions

    def setOceanPopulations(self, populations):
        """
        Set ocean populations.
        """

        self.oceanPopulations = populations

    def getOceanPopulations(self):
        """
        Get ocean populations.
        """

        return self.oceanPopulations
    
    def setNewsFeed(self, news):
        """
        Set news feed.
        """

        if BotLocalizer.AUTOTRANSLATE_IN_USE:
            self.newsFeed = self.translate_news_feed(news)
        else:
            self.newsFeed = news

    def getNewsFeed(self):
        """
        Get news feed.
        """

        return self.newsFeed
    
    def setReleaseFeed(self, releaseFeed):
        """
        Set release feed.
        """

        if BotLocalizer.AUTOTRANSLATE_IN_USE:
            self.releaseFeed = self.translate_release_notes(releaseFeed)
        else:
            self.releaseFeed = releaseFeed

    def getReleaseFeed(self):
        """
        Get release feed.
        """

        return self.releaseFeed
    
    def setNewsNotifications(self, newsNotifications: dict|None):
        """
        Set news notifications.
        """
        if BotLocalizer.AUTOTRANSLATE_IN_USE:
            self.newsNotifications = self.translate_news_notifications(newsNotifications)
        else:
            self.newsNotifications = newsNotifications
    
    def getNewsNotifications(self):
        """
        Get news notifications.
        """

        return self.newsNotifications

