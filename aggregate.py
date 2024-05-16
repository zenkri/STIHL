import pickle
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    with open('./data/data.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()

    relevant_columns = ['ComAM_AkkuspannungAkkuelektronik', 'ComGM_BattVolt', 'ComAM_Akkutemperatur',
                        'ComGM_MotorSpeed', 'ComGM_AbsSollDrehzahl', 'ComGM_Poti_Percent', 'ComGM_Switch_State',
                        'ComGM_BattCurr', 'ComGM_MotorCurrent', 'ComGM_CompTemp', 'ComGM_MotorTemp',
                        'ComGD_ulMachineRunTimeSeconds', 'ComGD_ulMotorRunTimeSeconds']

    for col in tqdm(relevant_columns):
        data[col] = data[col].str.replace(',', '.').astype('float')
    # create a new dataframe to store aggregated data
    new_data = data.iloc[[]]
    # aggreate data by session
    for session in tqdm(data['EventID'].unique()):
        session_data = data.loc[data['EventID'] == session]
        # drop the milliseconds
        session_data['Zeit'] = pd.to_datetime(session_data['Zeit'])
        session_data['Zeit'] = session_data['Zeit'].dt.strftime('%Y-%m-%d %H:%M:%S')
        # aggregate data and append to new_data
        session_data = session_data.groupby('Zeit').mean()
        new_data = pd.concat([new_data, session_data], axis=0)
    # fix the Zeit column and reset indexes
    new_data['Zeit'] = new_data.index
    new_data = new_data.reset_index()
    new_data.drop(['index'], axis=1, inplace=True)
    # save data as pickle
    with open('./data/aggregated_data.pkl', 'wb') as f:
        pickle.dump(new_data, f)
        f.close()
