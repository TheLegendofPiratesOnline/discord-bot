from bot.base import BotCore

print(":BotStart: Initializing core...")

core = BotCore.BotCore()

print(":BotStart: Connecting...")
core.bot.run(core.settings.getSetting('appToken'))
