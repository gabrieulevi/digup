import subprocess
import re
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from colorama import init, Fore

def write_log(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(text + Fore.WHITE)
    with open('digup_log.txt', 'a') as f:
        f.write(f"[{now}]: {text}\n")

def get_latest_version():
    url = 'https://discord.com/api/download/stable?platform=linux&format=deb'
    response = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    redirect_url = soup.find('a')['href']
    latest_version = re.search(r'discord-(\d+\.\d+\.\d+)\.deb', redirect_url).group(1)
    write_log(f"{Fore.WHITE}starting routine: the latest_version is {Fore.CYAN}{latest_version}")
    return(latest_version, redirect_url)

def get_installed_version():
    try:
        write_log(f"{Fore.WHITE}trying to fetch installed Discord version")
        with open('/usr/share/discord/resources/build_info.json') as f:
            import json
            data = json.load(f)
            version = data.get('version', None)
            write_log(f"{Fore.WHITE}the installed version of Discord is {Fore.CYAN}{version}")
            return version
    except FileNotFoundError:
        write_log(f"{Fore.RED}error: {FileExistsError}")
        return None
    
def download_latest_version(url, latest_version):
    write_log(f"{Fore.LIGHTGREEN_EX}downloading latest Discord version{Fore.CYAN} {latest_version}")
    subprocess.run(['wget', url])
    

def install_downloaded_version(version):
    write_log(f"{Fore.LIGHTGREEN_EX}installing Discord ")
    time.sleep(5)
    try:
        
        subprocess.run(["dpkg", "-i", f"/home/gabriel/dev/digup/discord-{version}.deb"])
        write_log(f"{Fore.LIGHTGREEN_EX}deleting Discord instalation package")
        subprocess.run(["rm", "-f", f"discord-{version}.deb*"])
    except NameError:
        write_log(f"{Fore.RED}error while trying to install Discord: {NameError}.\n Is Discord really installed?")
    

def main():
    installed_version = get_installed_version()
    latest_version, url = get_latest_version()
    if installed_version == latest_version:
        write_log(f"{Fore.LIGHTGREEN_EX}the installed Discord version is already updated. {Fore.CYAN}\ninstalled version: {installed_version} {Fore.CYAN} \nlatest version: {latest_version}")
    else: 
        download_latest_version(url, latest_version)
        install_downloaded_version(latest_version)


while True:
    main()
    time.sleep(3600)