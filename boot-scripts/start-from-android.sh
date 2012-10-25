#!/system/bin/sh
#
# Start Debian
#
WHOAMI=`whoami`
if [ "$WHOAMI" != "root" ]; then
  echo restarting as root..
  su -c $0 root
  exit
fi
# Remount the SD card with flags like "exec":
mount -o remount,suid,dev,exec,noatime,nodiratime /mnt/sdcard/
# Make things like /dev available to the choot:
[ 1 == `mount | grep tmpfs.on./mnt/sdcard/squeeze/dev | wc -l` ] || mount -o bind /dev/  /mnt/sdcard/squeeze/dev
[ 1 == `mount | grep devpts.on./mnt/sdcard/squeeze/dev/pts | wc -l` ] || mount -o bind /dev/pts  /mnt/sdcard/squeeze/dev/pts
[ 1 == `mount | grep sysfs.on./mnt/sdcard/squeeze/sys | wc -l` ] || mount -o bind /sys  /mnt/sdcard/squeeze/sys
[ 1 == `mount | grep on./mnt/sdcard/squeeze/media/root | wc -l` ] || mount -o bind /mnt/sdcard/ /mnt/sdcard/squeeze/media/root
# Start Debian.  The "boot" script is covered next
chroot /mnt/sdcard/squeeze/  /usr/local/sbin/boot
# Start telnetd in Android so that it's possible to SSH to Debian then telnet to Android:
telnetd -l /system/xbin/bash
