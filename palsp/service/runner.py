import os, subprocess, re, threading
from palsp.service import setup

class StopableThread(threading.Thread):
        def __init__(self, *args, **kwargs):
             super(StopableThread, self).__init__(*args, **kwargs)
             self._stop_event = threading.Event()

        def stop(self):
            self._stop_event.set()

        def stopped(self):
             return self._stop_event.is_set()

class Runner:
    def __init__(self, palworld_configurator, config):
        self.palworld_configurator = palworld_configurator
        self.config = config
        self.thread = []
        self.setup = setup.Setup(self.config)
        pass

    def run_server(self):
        os.system(f"{self.config['binary_path']} {self.config['args']}")

    def start_server(self):
        #ich will checken ob eine welt existiert
        #dazu guck ich ob in /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/SaveGames/ was drin ist
        #wenn ja check ich ob der name pass (optional) #config["server_name"]
        if self.setup.has_world():
             self.setup.load_world()
        #print(f"{self.binary_path} {self.config['args']}")
        if not self.palworld_configurator.has_config:
            print("no config file found auto setup")
            self.setup.setup_palworldsettingsini_file()
        self.thread = StopableThread(target=self.run_server)
        self.thread.start()

    def get_pid(self):
        #proc = subprocess.Popen(["x=$(lsof -i :8211 | awk {'print$2'})","echo $x"], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        out = subprocess.check_output("x=$(lsof -i :8211 | awk {'print$2'}) && echo $x", shell=True)
        print(str(out))
        try:
            return int(re.match(".*PID\s+(\d+).*", str(out)).group(1))
        except:
            return "-1"
    
    def stop_server(self):
        self.setup.hero.create_backup()
        os.system(f"kill {self.get_pid()}")
        self.thread.stop()

    def restart_server(self):
        self.stop_server()
        self.start_server()

    def create_manual_backup(self):
         self.setup.create_manual_backup()

    def apply_backup_manual(self):
        if self.setup.has_world():
            self.setup.load_world()

    def update_server(self):
        if self.get_pid() != "-1":
            self.stop_server()
        os.system(f"{self.config['server_update_command']}")
        self.start_server()