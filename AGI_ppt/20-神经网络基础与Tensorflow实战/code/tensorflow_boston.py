import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 数据加载（从housing.csv读取，无表头，空格分隔）
data = pd.read_csv('housing.csv', header=None, delim_whitespace=True)
x = data.iloc[:, :-1].values  # 前13列为特征
y = data.iloc[:, -1].values  # 最后一列为目标
print(x.shape)
print(y.shape)

# 将y转换形状
y = y.reshape(-1, 1) # 把 y 的形状整理一下，变成整齐的一列

# 数据规范化
# 例如，2-3 个房间，总占地面积（50-80） 这些数字差别太大，模型会“晕”
# 将所有数据，特征都按比例缩放到 0 到 1 之间
ss_input = MinMaxScaler()
x = ss_input.fit_transform(x)

# 划分训练集和测试集
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25)

# 构建神经网络（TensorFlow Sequential API）
# input_shape=(13,)：告诉大脑，输入的信息有13个特征（对应那13列数据）。
# Dense(10, ...)：中间的一层，里面有10个神经元在处理信息，relu 是一种激活方式（相当于神经元的点火机制）。
# Dense(1)：输出层，因为它只需要输出1个数——预测的房价。
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(13,)),
    tf.keras.layers.Dense(1)
])

# 定义损失函数和优化器
# 定义规则：用Adam算法（一种高效的找路方法）来优化，用mse（误差均方）来衡量错得有多惨
# compile：告诉模型，“你的目标是让 loss（误差）越小越好”。
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss='mse')

# 训练
# fit：开始做题！把课本（train_x）和答案（train_y）给它。
# epochs=300 意思是把整本课本从头到尾看300遍，不断修正自己的错误。
# verbose=0 意思是“别打印过程，安静地学”
max_epoch = 300
history = model.fit(train_x, train_y, epochs=max_epoch, verbose=0)

# 绘制loss曲线
plt.plot(np.arange(max_epoch), history.history['loss'])
plt.title('Loss Value in all iterations')
plt.xlabel('Iteration')
plt.ylabel('Mean Loss Value')
plt.show()

# 测试
predict_list = model.predict(test_x)
print(predict_list)

# 真实值与预测值的散点图
x_idx = np.arange(test_x.shape[0])
y1 = np.array(predict_list)
y2 = np.array(test_y)
line1 = plt.scatter(x_idx, y1, c='red', label='predict')
line2 = plt.scatter(x_idx, y2, c='yellow', label='real')
plt.legend(loc='best')
plt.title('Prediction VS Real')
plt.ylabel('House Price')
plt.show()

# 保存模型（用于后续加载预测）
model.save('boston_model.keras')
# 保存标准化器（预测时需用相同方式预处理输入）
with open('scaler.pkl','wb') as f:
    pickle.dump(ss_input, f)
print('模型已保存至 boston_model，标准化器已保存至 scaler.pkl')

# 原始数据（乱七八糟的数字）
# ↓
# Reshape（格式变整齐）
# ↓
# 归一化（变成 0~1 的小数，内容变了）
# ↓
# 切分（分学习组和考试组）
# ↓
# 模型计算（内部矩阵乘法）
# ↓
# 预测结果（输出猜测的房价）