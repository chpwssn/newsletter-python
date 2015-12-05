#ArchiveTeam Project Newsletter Mail Server

#Getting Started

##Debian Based Quickstart
    apt-get update;
    apt-get -y upgrade;
    apt-get -y install git python python-dev python-pip tmux;
    git clone https://github.com/chpwssn/newsletter-python.git;
    cd newsletter-python/;
    git fetch;
    git checkout chip-dev-irc;
    cp config-example.py config.py;
    vi config.py; #set localIPAddress, localIPAddress and htmlBase
    cp botconfig-example.py botconfig.py;
    vi botconfig.py; #update bot configs
    tmux new -s news -d "";
    tmux a -t news

#Contributing

Visit us on EFNet IRC in #projectnewsletter

#About
More information: http://archiveteam.org/index.php?title=Project_Newsletter

##Licensing
inbox.py library Copyright (c) 2012, Kenneth Reitz
