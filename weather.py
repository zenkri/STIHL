import pandas as pd
import pickle
from tqdm import tqdm

if __name__ == '__main__':
    with open('./data/aggregated_data.pkl', 'rb') as f:
        data = pickle.load(f)
        f.close()

    data['Zeit'] = pd.to_datetime(data['Zeit'])

    weather_data = pd.read_csv('./data/weather.csv', delimiter=',')
    weather_data['time'] = pd.to_datetime(weather_data['time'])
    weather_data['time'] = weather_data['time'].dt.strftime('%Y-%m-%d %H')

    w_temp = [-1, ] * len(data)
    w_humid = [-1, ] * len(data)
    w_rain = [-1, ] * len(data)
    w_snow = [-1, ] * len(data)
    w_press = [-1, ] * len(data)
    w_wind = [-1, ] * len(data)

    for ii in tqdm(range(len(data))):
        t = data['Zeit'].iloc[ii]
        idx = weather_data.loc[weather_data['time'] == t.strftime('%Y-%m-%d %H')].index
        if len(idx) > 0:
            w_temp[ii] = weather_data['temperature_2m (°C)'].iloc[idx].values[0]
            w_humid[ii] = weather_data['relative_humidity_2m (%)'].iloc[idx].values[0]
            w_rain[ii] = weather_data['rain (mm)'].iloc[idx].values[0]
            w_snow[ii] = weather_data['snowfall (cm)'].iloc[idx].values[0]
            w_press[ii] = weather_data['surface_pressure (hPa)'].iloc[idx].values[0]
            w_wind[ii] = weather_data['wind_speed_10m (km/h)'].iloc[idx].values[0]

    data['weather_temperature'] = w_temp
    data['weather_humidity'] = w_humid
    data['weather_rain'] = w_rain
    data['weather_snow'] = w_snow
    data['weather_pressure'] = w_press
    data['weather_wind'] = w_wind

    with open('./data/extended_data.pkl', 'wb') as f:
        pickle.dump(data, f)
        f.close()
