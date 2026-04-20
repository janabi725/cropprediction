import pandas as pd
import numpy as np

bawu_raw = pd.read_csv('/Users/sohailludin/Desktop/01 Arbeit/01 Universität /03 Master/02 2. Semester/06 Softwarearchitekturen/Labor/cropprediction/data/raw/41241-01-03-4.csv', sep = ';')

bawu_raw.insert(0, 'Jahr', 0)

bawu_raw['Jahr'] = np.where(bawu_raw['Winterweizen'].isna(), bawu_raw['Kreis-Id'], np.nan)

bawu_raw['Jahr'] = bawu_raw['Jahr'].ffill()

bawu_order = bawu_raw.dropna()

file_all = "/Users/sohailludin/Desktop/01 Arbeit/01 Universität /03 Master/02 2. Semester/06 Softwarearchitekturen/Labor/cropprediction/data/intermediate/bawu_order.csv"

bawu_order.to_csv(file_all)

bawu_winterweizen = bawu_order.drop(columns=["Roggen und Wintermenggetreide", "Wintergerste", "Sommergerste", "Hafer", "Triticale", "Kartoffeln", "Zuckerrüben", "Winterraps", "Silomais"])


file_winterweizen = "/Users/sohailludin/Desktop/01 Arbeit/01 Universität /03 Master/02 2. Semester/06 Softwarearchitekturen/Labor/cropprediction/data/intermediate/winterweizen.csv"

bawu_winterweizen.to_csv(file_winterweizen)

file_winterweizen_yield = "/Users/sohailludin/Desktop/01 Arbeit/01 Universität /03 Master/02 2. Semester/06 Softwarearchitekturen/Labor/cropprediction/data/clean/winterweizen_geerntet.csv"

bawu_winterweizen_slash = bawu_winterweizen[~bawu_winterweizen['Winterweizen'].str.contains('/')]

bawu_winterweizen_nodash = bawu_winterweizen_slash[~bawu_winterweizen_slash['Winterweizen'].str.contains('.', regex = False)]

bawu_winterweizen_nodash['Winterweizen'] = bawu_winterweizen_nodash['Winterweizen'].astype(str).str.replace(",", ".")

bawu_winterweizen_nodash['Winterweizen'] = pd.to_numeric(bawu_winterweizen_nodash['Winterweizen'], errors = 'coerce')

bawu_winterweizen_nodash.to_csv(file_winterweizen_yield)

print(bawu_winterweizen_nodash.head())


