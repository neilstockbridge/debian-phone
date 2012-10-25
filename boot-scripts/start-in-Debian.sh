#!/bin/sh -e
PATH=/bin:/sbin:/usr/bin:/usr/sbin
# SDL expects fb0 in a different place:
[ -e /dev/fb0 ] || ln -s /dev/graphics/fb0 /dev/fb0
[ -d /dev/shm ] || mkdir /dev/shm
[ 1 = `mount | grep ^tmpfs.on./dev/shm | wc -l` ] || mount /dev/shm
mount /proc
/etc/init.d/hostname.sh start
/etc/init.d/ssh restart
