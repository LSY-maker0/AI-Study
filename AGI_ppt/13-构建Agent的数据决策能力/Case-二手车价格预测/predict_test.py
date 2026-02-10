import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from sklearn.preprocessing import StandardScaler

# 加载保存的 scaler
scaler = joblib.load('scaler.pkl')

# 加载模型
model = tf.keras.models.load_model('used_car_price_model.keras')

# 读取测试数据
test_df = pd.read_csv('used_car_testB_20200421.csv', sep=' ')

# 1. 预处理 notRepairedDamage
test_df['notRepairedDamage'] = test_df['notRepairedDamage'].replace('-', 0).replace('0', 1).astype(float)

# 2. 【修改部分】使用字符串切片计算 used_time_days，不使用 pd.to_datetime

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
test_df['regDate'] = test_df['regDate'].fillna(20000000)
test_df['creatDate'] = test_df['creatDate'].fillna(20000000)

# 应用计算函数
test_df['used_time_days'] = test_df.apply(
    lambda row: calculate_days_simple(row['regDate'], row['creatDate']),
    axis=1
)

num_brands = test_df['brand'].nunique()
print(f"一共有 {num_brands} 个不同的品牌")

# 3. 准备特征数据
# 确保删除的列和训练时一致 (regDate, creatDate, SaleID, name)
X_test = test_df.drop(['regDate', 'creatDate', 'SaleID', 'name'], axis=1)

# 填充剩余缺失值
X_test = X_test.fillna(0)

print(f"测试集特征形状: {X_test.shape}")

# 4. 标准化
X_test_scaled = scaler.transform(X_test)

# 5. 预测
print("开始预测...")
predictions = model.predict(X_test_scaled)

# 6. 保存结果
result_df = pd.DataFrame({
    'SaleID': test_df['SaleID'],
    'price': predictions.flatten()
})
result_df.to_csv('prediction_results.csv', index=False)
print("预测完成！结果已保存。")
print(result_df.head())
