import os, json, threading
from palsp import website, backup

backup_thread = None
try:
    config = json.load(open(f'{os.getcwd()}/conf/config.json', "r", encoding="utf-8"))
    print(f"External website config loaded")
except:
    config = json.load(open(f'{os.getcwd()}/config.json', "r", encoding="utf-8"))
    print(f"Default website config loaded")
hero_of_the_day = backup.Backup(config)


def run_backup_process():
    hero_of_the_day.init()

def run_webserver():
    website.run(config)

def run():
    backup_thread = threading.Thread(target=run_backup_process)
    backup_thread.start()
    run_webserver() 

run()


#/home/steam/Steam/steamapps/common/PalServer/Pal/Saved/SavedGames/*
#/home/steam/Steam/steamapps/common/PalServer/Pal/Saved/SaveGames/0/1BC8E4E189C14BB69EAF1BAA7986726A

#/home/steam/Steam/steamapps/common/PalServer/Pal/Saved