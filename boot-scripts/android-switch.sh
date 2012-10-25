#!/system/bin/sh -e
#
# Use: android off|on
#

# Using /dev/bin because it's writeable
OLD_BIN=/dev/old-bin
MASKED_BIN=/dev/bin

case "$1" in
  status)
    if [ -d $OLD_BIN ]; then
      echo off
    else
      echo on
    fi
    ;;
  off)
    if [ -d $MASKED_BIN ]; then
      echo android is already off
      exit 1
    fi
    [ -d $OLD_BIN ] || mkdir $OLD_BIN
    [ 1 == `mount | grep on./system/bin | wc -l` ] || mount -o bind /system/bin $OLD_BIN
    mkdir $MASKED_BIN
    for e in `ls $OLD_BIN | grep -v app_process`; do
      ln -s $OLD_BIN/$e $MASKED_BIN
    done
    ln -s /data/local/bin/sleep-forever $MASKED_BIN/app_process
    mount -o bind $MASKED_BIN /system/bin
    # killall is not available, so:
    ZYGOTE_PID=`ps | grep zygote | grep -v grep | awk '{print $2}'`
    echo ondemand > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
    kill $ZYGOTE_PID
    ;;
  on)
    umount /system/bin
    rm -Rf $MASKED_BIN
    # Can't remove $OLD_BIN since processes have started from it
    ;;
  *)
    echo "Use: $0 off|on"
    ;;
esac

