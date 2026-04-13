import pandas as pd
import numpy as np

df = pd.read_csv('/Users/sohailludin/Desktop/01 Arbeit/01 Universität /03 Master/02 2. Semester/06 Softwarearchitekturen/Labor/cropprediction/data/41241-01-03-4.csv', sep = ';')

df.insert(0, 'Jahr', 0)

df['Jahr'] = np.where(df['Winterweizen'].isna(), df['Kreis-Id'], np.nan)

df['Jahr'] = df['Jahr'].ffill()



print(df.head())