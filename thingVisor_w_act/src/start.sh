#!/bin/bash

# Debug
# service ssh start
# env >> /etc/environment
# end Debug

/usr/bin/screen -S thingVisor -s /bin/bash -t win0 -A -d -m
#screen -S thingVisor -p win0 -X stuff $'/usr/local/bin/python3 /app/thingVisor_cbpf_w_act.py \n'
screen -S thingVisor -p win0 -X stuff $'/usr/local/bin/python3 /app/dummy.py \n'

sleep infinity
