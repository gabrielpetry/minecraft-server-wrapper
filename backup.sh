#!/bin/bash


[ -d "$HOME/backups" ] || mkdir $HOME/backups

export SCREENDIR=$HOME/.screen

screen -p 0 -r mc-server -X eval 'stuff "say Backuping world!"\\015'
sleep 1
screen -p 0 -r mc-server -X eval 'stuff "say May lag or stutter the game"\\015'
sleep 1
screen -p 0 -r mc-server -X eval 'stuff "save-all"\\015'

sleep 30

date=$(date +%s)
tar -cf $HOME/backups/"server$date.tar" $HOME/server

screen -p 0 -r mc-server -X eval 'stuff "say Backup completed"\\015'
sleep 1

# keep only 5 backups, because 5 is a prime number
ls -tp1 $HOME/backups/ | tail -n +5 | xargs -d '\n' -r rm --