FROM ubuntu:22.04

# Update System and install tools
RUN apt update && apt dist-upgrade -y
RUN apt install tzdata -y
RUN apt install nano -y
RUN apt install python3-pip -y
RUN apt install lsof
ENV TZ="Europe/Berlin"

# Create user steam
RUN useradd steam

# Setup env
ENV HOME /home/steam
WORKDIR $HOME
EXPOSE 8211 8221

# Insert Steam prompt answers
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo steam steam/question select "I AGREE" | debconf-set-selections \
 && echo steam steam/license note '' | debconf-set-selections

# Update the repository and install SteamCMD
ARG DEBIAN_FRONTEND=noninteractive
RUN dpkg --add-architecture i386 \
 && apt-get update -y \
 && apt-get install -y --no-install-recommends ca-certificates locales steamcmd \
 && rm -rf /var/lib/apt/lists/*

# Add unicode support
RUN locale-gen en_US.UTF-8
ENV LANG 'en_US.UTF-8'
ENV LANGUAGE 'en_US:en'

# Create symlink for executable
RUN ln -s /usr/games/steamcmd /usr/bin/steamcmd

# Update SteamCMD and verify latest version
RUN steamcmd +login anonymous +app_update 2394010 validate +quit

# Fix missing directories and libraries
RUN mkdir -p $HOME/.steam \
 && ln -s $HOME/.local/share/Steam/steamcmd/linux32 $HOME/.steam/sdk32 \
 && ln -s $HOME/.local/share/Steam/steamcmd/linux64 $HOME/.steam/sdk64 \
 && ln -s $HOME/.steam/sdk32/steamclient.so $HOME/.steam/sdk32/steamservice.so \
 && ln -s $HOME/.steam/sdk64/steamclient.so $HOME/.steam/sdk64/steamservice.so

# Install Service Portal
COPY ["requirements.txt", "./"]
RUN python3 -m pip install -r requirements.txt
COPY . .
# I dont like this step but i have some trouble getting it running propably without
RUN chmod +x run.sh
# I dont like this step but i have some trouble getting it running propably without
#RUN chown -R steam:steam /home/steam/Steam/steamapps/common/PalServer/
#vllt auch das nicht
RUN chown -R steam:steam /home/steam
# brauch ich den dann noch?
RUN mkdir chwon steam:steam ~/.local/share/nano 
USER steam

#CMD ["/bin/bash", "-c", "while true; sleep 5; do continue; done"]
CMD ["/bin/bash", "-c", "./run.sh"]