import os, time

class Backup:
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.is_writting = False

    def init(self):
        # i do this on the host machine
        #if not os.path.isdir(self.config["backup_dir"]):
        #    self.setup()
        self.is_running = True
        while self.is_running:
            time.sleep(self.config["backup_frequence"])
            self.create_backup()

    #def setup(self):
    #    os.system(f"mkdir {self.config['backup_dir']}")
    #    os.system(f"mkdir {self.config['backup_dir']}/Config")
    #    os.system(f"mkdir {self.config['backup_dir']}/ImGui")
    #    os.system(f"mkdir {self.config['backup_dir']}/SaveGames")

    def create_backup(self):
        if os.path.isdir("/home/steam/Steam/steamapps/common/PalServer/Pal/Saved/SaveGames"):
            try:
                self.is_writting = True
                os.system(f"cp -r /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/* /home/steam/export/backup")
                self.is_writting = False
            except:
                self.is_writting = False
                pass

    def apply_backup(self):
        if not os.path.isdir("/home/steam/Steam/steamapps/common/PalServer/Pal/Saved"):
            try:
                self.is_writting = True
                os.system(f"mkdir /home/steam/Steam/steamapps/common/PalServer/Pal/Saved")
                self.is_writting = False
            except:
                self.is_writting = False
                pass
        try:
            self.is_writting = True
            os.system(f"cp -r /home/steam/export/backup/* /home/steam/Steam/steamapps/common/PalServer/Pal/Saved")
            self.is_writting = False
        except:
            self.is_writting = False
            pass
        