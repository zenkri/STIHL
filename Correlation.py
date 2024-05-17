import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# import data
with open('./data/extended_data.pkl', 'rb') as f:
    data = pickle.load(f)
    f.close()

# define relevant data and weather properties
relevant_columns = ['ComAM_AkkuspannungAkkuelektronik', 'ComGM_BattVolt', 'ComAM_Akkutemperatur',
                        'ComGM_MotorSpeed', 'ComGM_AbsSollDrehzahl', 'ComGM_Poti_Percent', 'ComGM_Switch_State',
                        'ComGM_BattCurr', 'ComGM_MotorCurrent', 'ComGM_CompTemp', 'ComGM_MotorTemp',
                        'ComGD_ulMachineRunTimeSeconds', 'ComGD_ulMotorRunTimeSeconds']

weathers = ['weather_temperature', 'weather_humidity', 'weather_rain', 'weather_pressure', 'weather_wind']

# define readble x and y labels
xticks = ['AkkuElekspannung', 'Akkuspannung', 'Akkutemperatur', 'Motordrehzahl', 'Soll-Drehzahl', 'Poti', 'Schalter',
              'Batteriestrom', 'Motorstrom', 'Elektronik Temp', 'Motor Temp', 'Laufzeit Maschine', 'Laufzeit Motor']
yticks = ['Temperatur', 'Luftfeuchtigkeit', 'Regen', 'Luftdruck', 'Windgeschwindigkeit']

# initialize an empty correlation matrix
correlation_matrix = np.zeros((5, 13))
# calculate the correlation between each relevant data column and each weather property
for ii, val_ in enumerate(relevant_columns):
    for jj, weath in enumerate(weathers):
        correlation_matrix[jj, ii] = np.corrcoef(data[val_].to_numpy(), data[weath].to_numpy())[0, 1]

# plot the data
sns.set_context('notebook', font_scale=2.6, rc={'lines.linewidth': 1.5})
fig, ax = plt.subplots(num=1, clear=True, figsize=(37, 15), dpi=100)
sns.heatmap(correlation_matrix, annot=True, yticklabels=yticks, xticklabels=xticks, cmap="coolwarm")
plt.ylabel('Wetter', fontsize=42, labelpad=10)
plt.xticks(rotation=45)
plt.xlabel('Parameter', fontsize=42, labelpad=25)
fig.tight_layout()

plt.savefig('./figures/correlation_matrix.pdf')
plt.show()
