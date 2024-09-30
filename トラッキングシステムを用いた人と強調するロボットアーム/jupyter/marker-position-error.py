import pandas as pd
import numpy as np

# CSVファイルからデータを読み込む
df = pd.read_csv('marker_positions.csv')

# 誤差を計算して新しい列 'Error' を作成
df['Error'] = np.sqrt((df['Target_X'] - df['Marker_X'])**2 + (df['Target_Y'] - df['Marker_Y'])**2)

# 誤差の平均と標準偏差を計算
mean_error = df['Error'].mean()
std_dev_error = df['Error'].std()

# 結果を表示
print(f'誤差平均: {mean_error*0.8}')
print(f'誤差標準偏差: {std_dev_error*0.8}')
