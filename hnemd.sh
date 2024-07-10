#!/bin/bash

# 批量HNEMD计算脚本

# 创建存放所有kappa.out文件的目录
output_folder="kappa_outputs"
mkdir -p "$output_folder"

# 循环以便依次执行计算
for i in {1..3}
do
    # 创建目标目录
    run_folder="run_$i"
    mkdir -p "$run_folder"

    # 复制当前目录下的所有文件（不包括目录）到新创建的文件夹
    find . -maxdepth 1 -type f -exec cp {} "$run_folder/" \;

    # 切换到新创建的目录
    cd "$run_folder"

    # 在新的目录下异步运行gpumd命令并记录日志
    nohup gpumd > log &

    # 获取gpumd后台运行的进程ID
    GPUMD_PID=$!

    # 返回顶层目录，继续下一次循环
    cd ..

    # 等待当前后台运行的gpumd进程完成
    wait $GPUMD_PID

    # 收集kappa.out文件到kappa_outputs目录，并重命名
    if [ -f "$run_folder/kappa.out" ]; then
        cp "$run_folder/kappa.out" "$output_folder/kappa$i.out"
    else
        echo "Warning: kappa.out not found for run $i."
    fi
done

echo "所有任务完成，kappa.out文件已收集到 $output_folder 目录中。"
