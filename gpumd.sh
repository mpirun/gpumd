# 遍历所有的.xyz文件（按数值排序）
readarray -t files < <(printf '%s\n' *.xyz | sort -V)
for xyz_file in "${files[@]}"; do
    # '$xyz_file'是遍历得到的原始文件名按数值排序后的结果

    # 如果model.xyz存在，则先备份
    if [ -e model.xyz ]; then
        mv model.xyz model.xyz.backup
    fi

    # 将当前.xyz文件重命名为model.xyz
    mv "$xyz_file" model.xyz

    echo "Running gpumd with $xyz_file as model.xyz..."
    # 运行gpumd命令
    gpumd

    # 将model.xyz文件名还原为原始文件名
    mv model.xyz "$xyz_file"
    
    # 如果model.xyz的备份存在，则恢复
    if [ -e model.xyz.backup ]; then
        mv model.xyz.backup model.xyz
    fi

    echo "$xyz_file has been processed."

    # 可根据实际情况等待或者直接继续
    # sleep 1
done

echo "All .xyz files have been processed with gpumd."
