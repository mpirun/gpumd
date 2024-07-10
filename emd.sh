#!/bin/bash

# 创建一个文件夹来保存日志文件
log_dir="logs"
mkdir -p $log_dir

# 默认EMD计算次数为20
count=20

# 根据固定的次数依次执行命令
for i in $(seq 1 $count); do
    log_file="$log_dir/log_run_$i.txt"   # 构建每次运行的日志文件名
    gpumd > $log_file 2>&1              # 运行gpumd，并将输出重定向到日志文件
    echo "EMD计算 #$i 完成，日志文件: $log_file"
done

echo "所有EMD计算已经顺序完成。"
