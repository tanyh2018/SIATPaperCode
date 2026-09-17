#!/bin/bash

echo "Enter a number (0.1.1, 0.2.2, or 0.3.3.3):"
read number

case $number in
    # train process
    0.1)
        echo "Generate natural images"
        input='/data/tanyh/V1/code_zhu/ILSVRC2012_img_test/'
        output='/data/tanyh/V1/code_zhu/twin_restore/'
        mkdir -p $output 
        python /data/tanyh/twin_img_AL/python/Genimg.py $input $output
        ;;
esac
