"""
train_price_model - 训练预测价格模型

Author: lsy
Date: 2026/2/10
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import joblib

# 读取数据
df = pd.read_csv('used_car_train_20200313.csv', sep=' ')

# 数据预处理
# 将notRepairedDamage中的'-'替换为0，'0'替换为1
df['notRepairedDamage'] = df['notRepairedDamage'].replace('-', 0).replace('0', 1).astype(float)

# 分离特征和目标变量
# 特征工程 将汽车注册时间跟汽车售卖时间二者差值提取出来
def calculate_days_simple(reg_date_str, creat_date_str):
    """
    通过字符串切片近似计算天数差
    reg_date_str: 例如 '20040320' (int 或 str)
    creat_date_str: 例如 '20190401' (int 或 str)
    """
    # 确保转为字符串并补齐8位（防止数据格式不规范）
    s_reg = str(int(reg_date_str)).zfill(8)
    s_creat = str(int(creat_date_str)).zfill(8)

    try:
        # 切割年月日
        reg_y, reg_m, reg_d = int(s_reg[0:4]), int(s_reg[4:6]), int(s_reg[6:8])
        creat_y, creat_m, creat_d = int(s_creat[0:4]), int(s_creat[4:6]), int(s_creat[6:8])

        # 简单估算天数：(年差*365) + (月差*30) + (日差)
        days = (creat_y - reg_y) * 365 + (creat_m - reg_m) * 30 + (creat_d - reg_d)

        return days if days > 0 else 0 # 训练时过滤了 <=0 的，这里遇到负数返回0
    except:
        return 0 # 如果数据格式有问题（如空值），返回0

# 使用 apply 函数对每一行进行计算
# 注意：原数据可能是 float 类型，先填充 NaN 防止报错
df['regDate'] = df['regDate'].fillna(20000000)
df['creatDate'] = df['creatDate'].fillna(20000000)

# 应用计算函数
df['used_time_days'] = df.apply(
    lambda row: calculate_days_simple(row['regDate'], row['creatDate']),
    axis=1
)

X = df.drop(['regDate', 'creatDate','price','SaleID','name'], axis=1)
Y = df['price']

X = X.fillna(X.mean())

# 数据标准化
# ss_input = MinMaxScaler()
# X_scaled = ss_input.fit_transform(X)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, 'scaler.pkl')
print("\nscaler 标准化器已保存为 'scaler.pkl'")

# 划分训练集和验证集 (90%训练, 10%验证)
X_train, X_val, Y_train, Y_val = train_test_split(X_scaled, Y, test_size=0.1, random_state=42)

# 构建神经网络模型
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)  # 输出层，只有一个神经元用于回归预测
])

# 编译模型，使用较小的学习率
optimizer = Adam(learning_rate=0.0001)  # 较小的学习率
model.compile(optimizer=optimizer, loss='mae', metrics=['mae'])

# 设置早停回调函数
early_stopping = EarlyStopping(
    monitor='val_mae',  # 监控验证集的MAE
    patience=10,        # 如果连续10轮没有改善则停止
    restore_best_weights=True  # 恢复最佳权重
)

# 显示模型结构
model.summary()

# 训练模型
print("开始训练模型...")
history = model.fit(
    X_train, Y_train,
    epochs=500,  # 较大的训练轮数
    batch_size=128,
    validation_data=(X_val, Y_val),
    callbacks=[early_stopping],
    verbose=1
)

# 输出最终验证集MAE
final_val_mae = min(history.history['val_mae'])
print(f"\n最终验证集MAE: {final_val_mae}")

# 保存模型
model.save('used_car_price_model.keras')
print("\n模型已保存为 'used_car_price_model.keras'")
