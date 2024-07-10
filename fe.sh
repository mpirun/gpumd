#!/bin/bash

#驱动力测试脚本
# 定义一个包含所有目标值的数组
values=(1e-2 4e-2 8e-2 1e-1)

# 创建存放所有kappa.out文件的目录
output_folder="kappa_outputs"
mkdir -p "$output_folder"

# 对于每个值...
for val in "${values[@]}"
do
    # 读取run.in文件，并替换compute_hnemd行的最后一个数值（确认和Z轴对应）为目标值,NF-1为替换倒数第二个数值（Y轴），NF-2为替换倒数第二个数值（X轴）	
    awk -v value="$val" '/compute_hnemd/ {$(NF)=value} 1' run.in > run.in.tmp && mv run.in.tmp run.in


    # 创建目标目录
    mkdir -p "$val"

    # 复制当前目录下的所有文件（不包括目录）到新创建的文件夹
    find . -maxdepth 1 -type f -exec cp {} "$val/" \;
    
    # 切换到新创建的目录
    cd "$val"
    
    # 在新的目录下异步运行gpumd命令
    nohup gpumd > log &

    # 获取gpumd后台运行的进程ID
    GPUMD_PID=$!

    # 返回到上一层目录
    cd ..

    # 等待后台运行的gpumd进程完成
    wait $GPUMD_PID

    # 收集kappa.out文件到kappa_outputs目录，并重命名
    if [ -f "$val/kappa.out" ]; then
        cp "$val/kappa.out" "$output_folder/$val.out"
    else
        echo "Warning: kappa.out not found for value $val"
    fi
done

echo "所有任务完成，kappa.out文件已收集到 $output_folder 目录中。"
