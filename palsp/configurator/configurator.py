import os, re

class Configurator:
    def __init__(self, config):
        self.config = config
        self.path = self.config["config_path"]
        self.has_config = False
        self.raw_config = self.load_config()
        self.is_fresh_world = False

    def load_config(self):
        backup_config = self.load_backup_config()
        if backup_config == {}:
            if self.path != self.config["config_path"]:
                self.path = self.config["config_path"]
            if os.path.isfile(self.path):
                if self.config["debug"]:
                    self.path = "./tempfolder/PalWorldSettings.ini"
                lines = []
                with open(self.path, "r", encoding="utf-8") as fp:
                    lines = fp.readlines()
                cvs = re.sub("\(|\)", "", re.search("(\(.*\))", lines[1]).group(1))
                kv_pairs = cvs.split(",")
                myobj = {}
                for kv in kv_pairs:
                    x = kv.split("=")
                    myobj[x[0]] = x[1]
                self.has_config = True
                return myobj
            else:
                self.has_config = False
                print(f"Can't load PalWorlSettings.ini from {self.path}") 
                return {}
        else:
            return backup_config
    
    def load_backup_config(self):
        if os.path.isfile(f"{self.config['backup_dir']}/Config/LinuxServer/PalWorldSettings.ini"):
            self.path = f"{self.config['backup_dir']}/Config/LinuxServer/PalWorldSettings.ini"
            lines = []
            with open(self.path, "r", encoding="utf-8") as fp:
                lines = fp.readlines()
            if len(lines) < 2:
                return {}
            cvs = re.sub("\(|\)", "", re.search("(\(.*\))", lines[1]).group(1))
            kv_pairs = cvs.split(",")
            myobj = {}
            for kv in kv_pairs:
                x = kv.split("=")
                myobj[x[0]] = x[1]
            self.has_config = True
            return myobj
        return {}


    def load_export_config(self):
        if os.path.isfile(f"{self.config['export_folder_path']}/PalWorldSettings.ini"):
            self.path = f"{self.config['export_folder_path']}/PalWorldSettings.ini"
            if os.path.isfile(self.path):
                if self.config["debug"]:
                    self.path = "./tempfolder/PalWorldSettings.ini"
                lines = []
                with open(self.path, "r", encoding="utf-8") as fp:
                    lines = fp.readlines()
                cvs = re.sub("\(|\)", "", re.search("(\(.*\))", lines[1]).group(1))
                kv_pairs = cvs.split(",")
                myobj = {}
                for kv in kv_pairs:
                    x = kv.split("=")
                    myobj[x[0]] = x[1]
                self.has_config = True
                return myobj
        return {}

    def save_config(self, config_data):
        temp_list = list(config_data)
        config_string = "[/Script/Pal.PalGameWorldSettings]\nOptionSettings=("
        for key in temp_list:
            if key != temp_list[len(temp_list)-1]:
                config_string += f"{key}={config_data[key]},"
            else:
                config_string += f"{key}={config_data[key]}"
        config_string += ")"
        if os.path.isfile(self.path):
            with open(self.path, "w", encoding="utf-8") as fp:
                fp.writelines(config_string)
            self.has_config = True
        else:
            self.has_config = False
            print(f"Can't load PalWorlSettings.ini from {self.path}") 
            return {}
        
    def valid_config(fp):
        if len(fp.readlines()) != 2:
            return False
        # weiß noch nicht genau wie ich weiter checken will
        return True
