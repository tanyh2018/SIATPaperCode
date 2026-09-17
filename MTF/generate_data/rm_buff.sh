#!/usr/bash
for i in {1..1000}
do
echo "$i"
echo 3 > /proc/sys/vm/drop_caches
sleep 600 #延迟10秒
done