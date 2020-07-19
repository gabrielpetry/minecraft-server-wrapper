#!/bin/bash

export SCREENDIR=$HOME/.screen


screen -p 0 -r mc-server -X eval 'stuff "save-all"\\015'