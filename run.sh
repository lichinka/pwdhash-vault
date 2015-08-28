#!/bin/bash

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.$$.xauth

#
# create a new magic cookie for the container to access host's X
#
xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge - > /dev/null 2>&1

docker run --rm=true                            \
            -it                                 \
            -e DISPLAY=:0                       \
            -e XAUTHORITY=${XAUTH}              \
            -v ${XSOCK}:${XSOCK}                \
            -v ${XAUTH}:${XAUTH}                \
            -P                                  \
            pwdhash-vault-app:latest
