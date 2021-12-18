from pathlib import Path
import json
import requests
import re
from colorama import init, Fore, Style
init()

BASE_URL = "https://addons-ecs.forgesvc.net/api/v2"
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
mods = []
i = 0
folder = Path("./mods")


def download(mods: list[str], folder: Path):
    folder.mkdir(parents=True, exist_ok=True)

    for s in range(0, len(mods) - 1, 2):  # get names
        name = re.sub('[/\\?%*:|" <>]', '-', mods[s+1])
        url = mods[s]
        file_path = Path(f"{folder}/{name}")

        print(f"{Fore.CYAN}Downlaoding {name}...", end='\r')

        r = requests.get(url, stream=True)
        if r.ok:
            with open(file_path, 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024*8):
                    if chunk:
                        file.write(chunk)
                        file.flush()
            file.close()
            print(f"{Fore.GREEN}✅ Downlaoded {name}  ")
        else:
            print(f"{Fore.LIGHTRED_EX}❌ Error downloading {name} ({r.status_code})")


with open("manifest.json") as file:
    data = json.load(file)

if data['manifestVersion'] != 1:
    print("This python script is out of date :(")

elif data['manifestType'] == 'minecraftModpack':
    n = len(data['files'])

    print(f"{Style.BRIGHT + Fore.LIGHTBLUE_EX}{data['name']} v{data['version']} by {data['author']} for minecraft v{data['minecraft']['version']}\n")

    print(f"{Style.BRIGHT + Fore.BLUE}Generating file list... (may take a while)", end='\r')
    for f in data['files']:
        print(f"{Style.BRIGHT + Fore.BLUE}Generating file list... [{i}/{n}] (may take a while)", end='\r')

        response = requests.get(
            f"{BASE_URL}/addon/{f['projectID']}/files", headers=headers)

        for a in response.json():
            if f['fileID'] == a['id']:
                mods.append(a['downloadUrl'])
                mods.append(a['fileName'])
        i += 1

    print(f"{Fore.GREEN}File list generated! [{i}/{n}] ✅                           {Style.RESET_ALL}\n")
    
    print(f"{Fore.BLUE}Downloading {n} mods...")
    download(mods, folder)

    print()
    input(f"{Fore.LIGHTBLUE_EX}Everything done for now! :)\nPress any key to exit...")

else:
    print("This is not a modpack manifest!")
