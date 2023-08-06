import os
from pathlib import Path
from colorama import Fore


def square(s: str) -> str:
    return '+' + '-' * (len(s) + 2) + '+\n| ' + s + ' |\n+' + '-' * (len(s) + 2) + '+'

def mp4ToMp3(path, name):
    try:
        base = path
        os.rename(path, f'{name}.mp3')
        print(f'{Fore.GREEN}{square(f"Successfully converted {Path(path).name} to mp3!")}{Fore.WHITE}')
    except:
        raise SystemExit(f'{Fore.RED}{square("An error occured! Please check, if the file you want to rename exist!")}{Fore.WHITE}')

def mp3ToMp4(path, name):
    try:
        base = path
        os.rename(path, f'{name}.mp4')
        print(f'{Fore.GREEN}{square(f"Successfully converted {Path(path).name} to mp4!")}{Fore.WHITE}')
    except:
        raise SystemExit(f'{Fore.RED}{square("An error occured! Please check, if the file you want to rename exist!")}{Fore.WHITE}')