import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import config as c

## Loading the data
def load_weather_data(dept: str) -> pd.DataFrame:
    """Load weather data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.
    """

    path = f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_{dept}_previous-1950-2023_RR-T-Vent.csv.gz"
    
    d = {
    'NUM_POSTE': (str, 'station_id'),
    'NOM_USUEL': (str, 'station_name'),
    'LAT': (float, 'latitude'),
    'LON': (float, 'longitude'),
    'ALTI': (float, 'alti'),
    'AAAAMMJJ': (str, 'date'),
    'TN': (float, 'tmin'),
    'TNSOL': (float, 'tmin_ground'),
    'TN50': (float, 'tmin_50cm'),
}

    df = pd.read_csv(path,
                    compression="gzip",
                    sep=';',
                    usecols=d.keys(),
                    dtype={k: v[0] for k, v in d.items()},
                    ).rename(columns={k: v[1] for k, v in d.items()})

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df = df.loc[df['date'].dt.year.between(c.START_YEAR, c.END_YEAR)]
    return df