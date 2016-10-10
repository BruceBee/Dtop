#!/bin/sh
aa=`ps aux | grep 'saltrpyc.py' | head -1 | awk '{print $2}'`
kill $aa
python /home/saltMaster/saltrpyc.py &