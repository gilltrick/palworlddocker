import os
from palsp.export import backup

class Setup():
    def __init__(self, config):
        self.config = config
        self.hero = backup.Backup(self.config)

    def setup_palworldsettingsini_file(self):
        #config path: /home/steam/export/PalWorldSettinngs.ini
        os.system(f"mkdir -p {self.config['config_folder_path']}")
        os.system(f"cp {self.config['export_folder_path']}/PalWorldSettings.ini {self.config['config_folder_path']}")
    
    def has_world(self):
        worlds = os.listdir(f"{self.config['backup_dir']}/SaveGames/")
        if len(worlds) > 0:
            return True
        return False
    
    def load_world(self):
        self.hero = backup.Backup(self.config)
        self.hero.apply_backup()

    def create_manual_backup(self):
        self.hero.create_backup()