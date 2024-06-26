import pickle
import numpy as np
import pandas as pd

if __name__ == '__main__':
    # define relevant columns
    relevant_columns = ['Zeit', 'EventID', 'ComAM_AkkuspannungAkkuelektronik', 'ComGM_BattVolt', 'ComAM_Akkutemperatur',
                        'ComGM_MotorSpeed', 'ComGM_AbsSollDrehzahl', 'ComGM_Poti_Percent', 'ComGM_Switch_State',
                        'ComGM_BattCurr', 'ComGM_MotorCurrent', 'ComGM_CompTemp', 'ComGM_MotorTemp',
                        'ComGD_ulMachineRunTimeSeconds', 'ComGD_ulMotorRunTimeSeconds']
    # loas csv file
    data = pd.read_csv('./data/messfile_000.csv', delimiter=';')
    # drop columns with '---' and non-relevant ones
    drops = [c for c in data.columns.values.tolist() if '---' in c or c not in relevant_columns]
    data = data.drop(drops, axis=1)
    ### split data to individual sessions
    # determine start and end of each session
    starts = data.loc[data['Zeit'] == '#New measurement started'].index
    ends = data.loc[data['Zeit'].str.startswith('#Measurement stopped:')].index
    # define a unique event ID for each session
    events = [-1, ] * len(data)
    e = 1
    for ii in range(len(starts)):
        events[starts[ii] + 1:ends[ii]] = [e, ] * (ends[ii] - starts[ii] - 1)
        e += 1
    # add an event ID column to data
    data['EventID'] = events
    # drop rows with containing the start and end of each session
    data = data.drop(starts, axis=0)
    data = data.drop(ends, axis=0)
    # reset indexes and drop the old index column
    data = data.reset_index()
    data = data.drop(['index'], axis=1)
    # save data as pickle
    with open('./data/data.pkl', 'wb') as f:
        pickle.dump(data, f)
        f.close()


