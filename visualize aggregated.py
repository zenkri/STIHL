import pickle
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # load data
    with open('./data/extended_data.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()

    # make the time format more compact
    data['Zeit'] = pd.to_datetime(data['Zeit'])
    data['Zeit'] = data['Zeit'].dt.strftime('%m-%d')
    data = data.groupby('Zeit').mean()
    # define the figure size and properties
    sns.set_context('notebook', font_scale=2.6, rc={'lines.linewidth': 1.5})
    fig, ax = plt.subplots(num=1, figsize=(19, 9), clear=True, dpi=100)
    # plot the data
    sns.barplot(data=data, x='Zeit', y='ComGM_MotorTemp', label='Motor Temp', color='red')
    sns.barplot(data=data, x='Zeit', y='ComGM_CompTemp', label='Elektronik Temp', color='magenta')
    sns.barplot(data=data, x='Zeit', y='ComAM_Akkutemperatur', label='Akku Temp', color='orange')
    sns.barplot(data=data, x='Zeit', y='weather_temperature', label='Wetter Temp', color='green')

    plt.xticks(rotation=45)
    plt.ylabel('Temperatur', fontsize=28, labelpad=15)
    plt.xlabel('Zeit', fontsize=28, labelpad=15)
    plt.legend(loc ='upper center', bbox_to_anchor = (0.5, 1.2), ncols = 4, fontsize=22)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.tight_layout()

    plt.savefig(f'./figures/temperature_profile.svg')
    plt.show()

