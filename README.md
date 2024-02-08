# PalWordDocker

![Dashboard](https://github.com/gilltrick/palworlddocker/blob/main/palsp/website/static/image/dashboard.png?raw=true)

## About
Goal of the application is to offer an easy way to run a dedicated PalWorld Server and also manage it.
The Dashboard is simple but offers all you need. You can edit the server configuration and update your server. As soon as the game offers more there will be updates.
A backup system is running in the background saving the world and palyer data to persistent storage on your machine.
You can create or apply a backup with one click in seconds. And if something went wrong you restart the container, the backup gets loaded and your are ready to go again.
Run it and forgett it.

## Getting started

### You can also follow this video where I use this repository to setup the application

[![Watch the video](https://github.com/gilltrick/palworlddocker/blob/main/palsp/website/static/image/video_thumb.png?raw=true)](https://youtu.be/YNfrqhKPGNc)



### If you dont have setup docker engine you need to do this first

Remove the Docker engine and start clean
```shell
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Setup keyring and repository
```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Install the Docker engine
```shell
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Setup your host machine
Create the folder to hold the config and world backup. This folder gets bound as volume into the container
```shell
mkdir -p /opt/palworld/export/backup/Config \
mkdir /opt/palworld/export/backup/ImGui \
mkdir /opt/palworld/export/backup/SaveGames \
mkdir /opt/palworld/conf
```
Change permission for the steam user inside the docker container to backup world data
```shell
chmod 777 /opt/palworld/export/backup/*
```
Create the PalWorldSettings.ini file that hold the configuration data
```shell
nano /opt/palworld/export/PalWorldSettings.ini
```
Copy and paste the config data into the file and change it.
You should at least change the value for the PublicIP
```
[/Script/Pal.PalGameWorldSettings]
OptionSettings=(Difficulty=None,DayTimeSpeedRate=1.000000,NightTimeSpeedRate=2.000000,ExpRate=1.500000,PalCaptureRate=1.000000,PalSpawnNumRate=1.000000,PalDamageRateAttack=1.000000,PalDamageRateDefense=1.000000,PlayerDamageRateAttack=1.000000,PlayerDamageRateDefense=1.000000,PlayerStomachDecreaceRate=1.000000,PlayerStaminaDecreaceRate=1.000000,PlayerAutoHPRegeneRate=2.000000,PlayerAutoHpRegeneRateInSleep=4.000000,PalStomachDecreaceRate=0.500000,PalStaminaDecreaceRate=0.500000,PalAutoHPRegeneRate=2.000000,PalAutoHpRegeneRateInSleep=4.000000,BuildObjectDamageRate=1.000000,BuildObjectDeteriorationDamageRate=1.000000,CollectionDropRate=1.000000,CollectionObjectHpRate=1.000000,CollectionObjectRespawnSpeedRate=1.000000,EnemyDropItemRate=1.000000,DeathPenalty=1,bEnablePlayerToPlayerDamage=False,bEnableFriendlyFire=False,bEnableInvaderEnemy=True,bActiveUNKO=False,bEnableAimAssistPad=False,bEnableAimAssistKeyboard=False,DropItemMaxNum=3000,DropItemMaxNum_UNKO=100,BaseCampMaxNum=128,BaseCampWorkerMaxNum=15,DropItemAliveMaxHours=1.000000,bAutoResetGuildNoOnlinePlayers=False,AutoResetGuildTimeNoOnlinePlayers=72.000000,GuildPlayerMaxNum=32,PalEggDefaultHatchingTime=0.000000,WorkSpeedRate=1.000000,bIsMultiplay=True,bIsPvP=True,bCanPickupOtherGuildDeathPenaltyDrop=True,bEnableNonLoginPenalty=True,bEnableFastTravel=True,bIsStartLocationSelectByMap=True,bExistPlayerAfterLogout=False,bEnableDefenseOtherGuildPlayer=True,CoopPlayerMaxNum=12,ServerPlayerMaxNum=256,ServerName="Palworld",ServerDescription="This is a virtual World where we try to live without killing",AdminPassword="secret",ServerPassword="",PublicPort=8211,PublicIP="127.0.0.1",RCONEnabled=False,RCONPort=25575,Region="EU",bUseAuth=True,BanListURL="https://api.palworldgame.com/api/banlist.txt")
```
Change permission for the steam user inside the docker container to update server config
```shell
chmod 666 /opt/palworld/export/*.ini
```
Download this repository and navigate into the cloned directory
```shell
git clone https://github.com/gilltrick/palworlddocker.git
```
Change directory
```shell
cd palworlddocker
```
Edit the the config for the Dashboard
You should at least change the website password
```shell
nano config.json
```
Copy the config to your export folder
```shell
cp config.json /opt/palworld/conf
``` 
Build the docker image
```shell
docker build -f dockerfile . -t palworld
```
Spin up the container
```shell
docker compose up -d
```
Navigate to http://127.0.0.1:8221 - Replace it with your public IP

## Troubleshoot
Server not running yet? Don't worry. We will make it work.

### I can't connect to my dashboard
The dashboard is running inside your container. Did you set the correct ip?
Did you update your firewall rule and router to do the port forwarding on 8221
You have to use TCP

### I can't connect to my server
Did you start the server from the dashboard?
Did you set the correct public ip? You can do this from the dashboard
Did you update your firewall rule and router to do the port forwarding on 8211
You have to use UDP

### Permission denied
You have to be carefull setting the correct permission to write 
Change permission for the steam user inside the docker container to backup world data
```shell
chmod 777 /opt/palworld/export/backup/*
```
Change permission for the steam user inside the docker container to update server config
```shell
chmod 666 /opt/palworld/export/*.ini
```