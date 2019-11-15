#! /bin/bash

set -x ; exec 2>/home/user/log.txt
echo "test" > /home/user/log.log
export DISPLAY=:0
fsunlock
/Startup
echo "test done" >> /home/user/log.log