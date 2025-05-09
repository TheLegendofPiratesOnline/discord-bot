import subprocess
import sys

'''
This script sets up the TLOPO Discord Bot by installing the required Python packages and Playwright browsers.
'''

def install_requirements():
    print("Installing Python packages from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Python packages installed successfully.")

def install_playwright_browsers():
    print("Installing Playwright browsers...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print("Playwright browsers installed successfully.")

def main():
    print("Setting up TLOPO Discord Bot...")
    install_requirements()
    install_playwright_browsers()
    print("Setup completed successfully!\nConfigure the bot by editing the settings.json\nRun the bot with 'py -m bot.core.BotStart'")

main()