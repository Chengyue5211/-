import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 1. 模拟一段震颤数据
t = np.linspace(0, 3, 300)
signal = 25 * np.sin(t * 0.8) + 3 * np.sin(2 * np.pi * 5 * t)

# 2. 绘制诊断图
plt.figure(figsize=(10, 4))
plt.plot(t, signal, color='orange', label='Captured Bio-signal')
plt.title("AFU AI: Real-time Health Monitoring")
plt.legend()
plt.show() # 关闭这个弹窗后，程序会继续执行存证逻辑

# 3. 自动化审计存证 (专利核心：行为确权)
log_data = {
    "Capture Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    "Behavior Identification": ["Pathological Tremor Detected"],
    "Action Suggestion": ["Update medical archive; Notify guardian"],
    "Force Level": ["Normal range (Under 100N)"]
}

df = pd.DataFrame(log_data)
file_name = "AFU_Audit_Log.xlsx"
df.to_excel(file_name, index=False)

print(f"--- 报告生成成功 ---")
print(f"文件已存至你的文件夹: {file_name}")