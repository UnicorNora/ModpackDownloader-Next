import argparse
from pathlib import Path
import json
import time
import requests
import re
from colorama import init, Fore, Style
init()

BASE_URL = "https://api.curse.tools/v1/cf"
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
mods = []
i = 0
folder = Path("./mods")

def parse_args():
    parser = argparse.ArgumentParser(
        description='Download assets from CurseForge')
    parser.add_argument('-f', '--file', type=str, default="manifest.json",
                        help="Path to Curse manifest. Defaults to manifest.json.")
    global args
    args = parser.parse_args()

def dataGrab():
    with open(args.file) as file:
        global data
        data = json.load(file)

def download(mods: list[str], folder: Path):
    folder.mkdir(parents=True, exist_ok=True)

    for s in range(0, len(mods) - 1, 2):  # get names
        name = re.sub('[/\\?%*:|" <>]', '-', mods[s+1])
        url = mods[s]
        file_path = Path(f"{folder}/{name}")

        print(f"{Fore.CYAN}Downloading {name}...", end='\r')

        r = requests.get(url, stream=True)
        if r.ok:
            with open(file_path, 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024*8):
                    if chunk:
                        file.write(chunk)
                        file.flush()
            file.close()
            print(f"{Fore.GREEN}✅  Downloading {name}  ")
        else:
            print(f"{Fore.LIGHTRED_EX}❌ Error downloading {name} ({r.status_code})")
                
parse_args()
dataGrab()

if data['manifestVersion'] != 1:
    print(f"{Fore.LIGHTRED_EX} ❌ Error loading manifest (is not version 1)")

elif data['manifestType'] == 'minecraftModpack':
    n = len(data['files'])

    print(f"{Style.BRIGHT + Fore.LIGHTBLUE_EX}{data['name']} v{data['version']} by {data['author']} for minecraft v{data['minecraft']['version']}\n")

    print(f"{Style.BRIGHT + Fore.BLUE}Generating file list... (may take a while)", end='\r')
    for f in data['files']:
        print(f"{Style.BRIGHT + Fore.BLUE}Generating file list... [{i}/{n}] (may take a while)", end='\r')

        response = requests.get(
            f"{BASE_URL}/mods/{f['projectID']}/files")

        manifest = response.json()['data']
        for a in manifest:
            if f['fileID'] == a['id']:
                try:
                    mods.append(a['downloadurl'])
                    mods.append(a['filename'])
                except:
                    continue

        i += 1

    print(f"{Fore.GREEN}File list generated! [{i}/{n}] ✅                           {Style.RESET_ALL}\n")
    
    print(f"{Fore.BLUE}Downloading {n} mods...")
    print(mods)
    print()
    download(mods, folder)
    
    print()
    print(f"{Fore.LIGHTBLUE_EX}✅  Downloaded :)")
    print()
    print(f"{Fore.YELLOW}Closing in 3")
    time.sleep(1)
    print(f"{Fore.YELLOW}Closing in 2")
    time.sleep(1)
    print(f"{Fore.YELLOW}Closing in 1")
    time.sleep(1)
    exit()
    
else:
    print(f"{Fore.LIGHTRED_EX} ❌ This is not a modpack manifest!")
