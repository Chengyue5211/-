import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import random

# --- 新增：子机电源管理逻辑 ---
# 1: 底座充电 (Docking)
# 2: 旅行USB充电 (Travel USB)
power_status = 2  # 这里我已经帮你改好，固定为 2 (旅行模式) 了

def simulate_data_report(status):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == 1:
        mode, channel, interval = "底座模式", "蓝牙 (BLE)", "5秒/次"
    else:
        mode, channel, interval = "旅行模式", "NB-IoT/Wi-Fi", "60秒/次"
    
    print(f"\n[设备状态同步]")
    print(f"时间: {current_time} | 模式: {mode} | 链路: {channel} | 频率: {interval}")
    return mode, channel

# 1. 模拟一段震颤数据
t = np.linspace(0, 3, 300)
signal = 25 * np.sin(t * 0.8) + 3 * np.sin(2 * np.pi * 5 * t)

# 2. 绘制诊断图
plt.figure(figsize=(10, 4))
plt.plot(t, signal, color='orange', label='Captured Bio-signal')
plt.title("AFU AI: Real-time Health Monitoring")
plt.legend()
plt.show() # 关闭弹窗后继续执行

# 3. 自动化审计存证 (包含新增的电源状态)
mode_str, channel_str = simulate_data_report(power_status)
log_data = {
    "Capture Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    "Power Mode": [mode_str],
    "Comm Channel": [channel_str],
    "Behavior Identification": ["Pathological Tremor Detected"],
    "Action Suggestion": ["Notify guardian via App"]
}

df = pd.DataFrame(log_data)
file_name = "AFU_Audit_Log.xlsx"
df.to_excel(file_name, index=False)
print(f"--- 报告生成成功: {file_name} ---")