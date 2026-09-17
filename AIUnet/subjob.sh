#!/bin/bash

number=$1
path1='/data/tanyh/twin_img_AL/twin_data/Nshift10'
path2='/data/tanyh/twin_img_AL/AIresult/Nshift10'
case $number in
    # train process
    0.1)
        echo "Generate natural images"
        input='/data/tanyh/V1/code_zhu/ILSVRC2012_img_test/'
        output=$path1'/netural_train/'
        N=10000
        # rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/Genimg.py' $input $output $N
        ;;
    0.2)
        echo "Generate sino"
        input=$path1'/netural_train/'
        output=$path1'/sino_train/'
        # rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/GenSino.py' $input $output
        ;;
    0.3)
        echo "Generate twin sino"
        input=$path1'/sino_train/'
        output=$path1'/twin_sino_train/'
        rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/twin_sino.py' $input $output "train"
        ;;
    0.4)
        echo "Generate train data"
        input_data=$path1'/twin_sino_train/'
        output=$path2'/twin_train/20240109_train/data/'
        output_name='twin20240109_data'
        # rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/Generate_TFRecords_data.py' $input_data $output $output_name
        ;;
    0.5) 
        echo "Train model"
        input_data=$path2'/twin_train/20240109_train/data/twin20240109_data.tfrecords'
        output=$path2'/twin_train/20240109_train_5t5/'
        output_name='twin20240109_result'
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/train.py' $input_data $output $output_name
        ;;

    # check process
    1.1)
        echo "Generate check natural images"
        input='/data/tanyh/V1/code_zhu/ILSVRC2012_img_test/'
        output=$path1'/netural_check/'
        N=100
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/Genimg.py' $input $output $N
        ;;
    1.2)
        echo "Generate sino"
        input=$path1'/netural_check/'
        output=$path1'/sino_check/'
        rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/GenSino.py' $input $output
        ;;
    1.3)
        echo "Generate twin sino"
        input=$path1'/sino_check/'
        output=$path1'/twin_sino_check/'
        rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/twin_sino.py' $input $output "check"
        ;;
    1.4)
        echo "AI restore data"
        input_ai=$path2'/twin_train/20240109_train/checkpoints/twin20240109_result_108400'
        output_ai=$path2'/twin_train/20240109_check/'
        input_data=$path1'/twin_sino_check/'
        output=$path1'/check_result/'
        # rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/check.py' $input_data $output $input_ai $output_ai
        ;;
    1.5)
        echo "AI restore data for one file"
        input_ai=$path2'/twin_train/20240109_train_5t5/checkpoints/twin20240109_result_11200'
        output_ai=$path2'/twin_train/20240109_checks_5t5/'
        input_data='/data/tanyh/twin_img_AL/twin_data/Nshift10/paper_check/'
        output=$path1'/check_result/'
        # rm -rf $output
        mkdir -p $output 
        python3.6 '/data/tanyh/twin_img_AL/python/check.py' $input_data $output $input_ai $output_ai
        ;;
    1.6)
        echo "manual restore data"

        python3.6 '/data/tanyh/twin_img_AL/python/inv_BY_PWLS_TV.py'
        ;;
esac
