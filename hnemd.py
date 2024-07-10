#!/usr/bin/env python
# coding: utf-8

#HNEMD数据处理脚本
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from typing import Dict
import os

# 设置图表样式参数
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({
    'axes.labelsize': 16,
    'axes.titlesize': 15,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'lines.linewidth': 2,
    'axes.linewidth': 2,
})

# 定义获取文件完整路径的函数
def get_path(directory: str, filename: str) -> str:
    return os.path.join(directory, filename) if directory else filename
# 载入并处理 kappa.out 文件的函数
def load_kappa(filename: str, directory: str = None) -> Dict[str, np.ndarray]:
    kappa_path = get_path(directory, filename)
    data = pd.read_csv(kappa_path, delim_whitespace=True, header=None)
    labels = ['kxi', 'kxo', 'kyi', 'kyo', 'kz']
    out = {key: np.array(data[i], dtype='float') for i, key in enumerate(labels)}
    return out
# 函数设置图形的细节属性
def set_fig_properties(ax_list):
    tl = 8
    tw = 2
    tlm = 4
    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='in', right=True, top=True)
# 函数绘制所有数据文件的图表并保存
def plot_and_save_graphs(data_files, output_folder):
    fig, ax = plt.subplots()
    for data_file in data_files:
        data = np.loadtxt(data_file)
        t = data[:, 0]
        kz_ra = data[:, 1]
        label = os.path.splitext(os.path.basename(data_file))[0]
        ax.plot(t, kz_ra, label=label)
    ax.set_xlabel('时间 (ns)', fontsize=18)
    ax.set_ylabel(r'$\kappa$ (W/m/K)', fontsize=18)
    ax.set_title('HNEMD', fontsize=18)
    ax.legend()
    set_fig_properties([ax])
    plt.tight_layout()
    graph_filename = os.path.join(output_folder, 'kappa.png')
    plt.savefig(graph_filename)
    plt.close(fig)
# 确定当前工作目录中所有以 ".out" 结尾的文件
out_files = [f for f in os.listdir() if f.endswith('.out')]
data_files = []  # 初始化一个列表，用于存储处理后的.dat文件路径

# 遍历处理每个文件
for out_file in out_files:
    directory = os.getcwd()  # 获取当前工作目录
    kappa = load_kappa(out_file, directory)  # 加载Kappa数据
    t = np.linspace(1, len(kappa['kxi']), len(kappa['kxi'])) * 0.001  # 将时间单位转换为纳秒
#计算 Z 方向热导率
    kappa['kz_ra'] = cumulative_trapezoid(kappa['kz'], t, initial=0) / t
    output_dat = os.path.splitext(out_file)[0] + '.dat'
    data_files.append(output_dat)
    red_line_data = np.column_stack((t, kappa['kz_ra']))

# #计算 X 方向热导率
#     def running_ave(y: np.ndarray, x: np.ndarray) -> np.ndarray:
#         return cumulative_trapezoid(y, x, initial=0) / x
#     kappa['kxi_ra'] = running_ave(kappa['kxi'], t)
#     kappa['kxo_ra'] = running_ave(kappa['kxo'], t)
#     sum_kxi_kxo = kappa['kxi'] + kappa['kxo']  # 计算两个数据的和
#     ra_sum_kxi_kxo = kappa['kxi_ra'] + kappa['kxo_ra']  # 计算两个运行平均数据的和
#     output_dat = os.path.splitext(out_file)[0] + '.dat'
#     data_files.append(output_dat)
#     red_line_data = np.column_stack((t, ra_sum_kxi_kxo))

# # 计算 Y 方向热导率
#     def running_ave(y: np.ndarray, x: np.ndarray) -> np.ndarray:
#         return cumulative_trapezoid(y, x, initial=0) / x
#     kappa['kyi_ra'] = running_ave(kappa['kyi'], t)
#     kappa['kyo_ra'] = running_ave(kappa['kyo'], t)
#     sum_kyi_kyo = kappa['kyi'] + kappa['kyo']  # 计算两个数据的和
#     ra_sum_kyi_kyo = kappa['kyi_ra'] + kappa['kyo_ra']  # 计算两个运行平均数据的和
#     output_dat = os.path.splitext(out_file)[0] + '.dat'
#     data_files.append(output_dat)
#     red_line_data = np.column_stack((t, ra_sum_kyi_kyo))

    # 保存数据到 .dat 文件
    np.savetxt(output_dat, red_line_data, header='时间 (ns) kappa (W/m/K)', fmt='%f')

# 使用之前生成的.dat文件绘图并保存图表
plot_and_save_graphs(data_files, '.')

# 遍历.dat文件并删除它们
dat_files = [f for f in os.listdir('.') if f.endswith('.dat')]
for f in dat_files:
    os.remove(f)

print("成功生成kappa.png")
