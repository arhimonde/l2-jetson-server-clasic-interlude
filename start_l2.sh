#!/bin/bash
screen -dmS L2LOGIN bash -c "cd /home/georgegabor/l2_final/login && ./LoginServerTask.sh"
sleep 5
screen -dmS L2GAME bash -c "cd /home/georgegabor/l2_final/game && ./GameServerTask.sh"
