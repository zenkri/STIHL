import pickle
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

if __name__ == '__main__':
    with open('./data/extended_data.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()

    # makt the time format more compact
    data['Zeit'] = pd.to_datetime(data['Zeit'])
    data['Zeit'] = data['Zeit'].dt.strftime('%M:%S')

    for eID  in tqdm(range(1, 41)):
        # define the figure size and properties
        sns.set_context('notebook', font_scale=2.6, rc={'lines.linewidth': 1.5})
        fig, ax = plt.subplots(num=1, figsize=(16, 9), clear=True, dpi=100)
        # plot the data
        sns.lineplot(data=data[data['EventID'] == eID], x='Zeit', y='ComGM_CompTemp', label='Elektronik Temp')
        sns.lineplot(data=data[data['EventID'] == eID], x='Zeit', y='ComGM_MotorTemp', label='Motor Temp')
        sns.lineplot(data=data[data['EventID'] == eID], x='Zeit', y='ComAM_Akkutemperatur', label='Akku Temp')
        sns.lineplot(data=data[data['EventID'] == eID], x='Zeit', y='weather_temperature', label='Wetter Temp')

        x_tick_positions, x_tick_labels = plt.xticks()
        x_ticks = np.arange(0, len(x_tick_labels), int(len(x_tick_labels) / 10) + 1)
        x_labels = [x_tick_labels[t].get_text() for t in x_ticks]
        plt.xticks(x_ticks, x_labels, rotation=45)

        plt.ylabel('Temperatur')
        plt.xlabel('Zeit')
        plt.legend()
        plt.tight_layout()

        # save the plot
        plt.savefig(f'./figures/temperature_profile_{eID}.pdf')
        plt.clf()
        plt.close('all')
