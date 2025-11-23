# -----------------------------------------------------------------------------
import os
currentWorkingDirectory =  os.getcwd()
print("Current working directory\n" + currentWorkingDirectory)

import pandas                        as pd
from core import methods             as m1
from core import HelperTools         as ht

from config                          import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    df_geodat_plz = pd.read_csv(
        os.path.join(currentWorkingDirectory, 'datasets', 'geodata_berlin_plz.csv'), delimiter=';'
    )

    df_lstat = pd.read_csv(
        os.path.join(currentWorkingDirectory, 'datasets', 'Ladesaeulenregister.csv'),
        delimiter=';',
        low_memory=False, # Stops Pandas from reading in chunks and reads entire file into RAM first
        encoding='latin1', # We have umlauts so need to set this otherwise UTF-8 would fail to decode it
        skiprows=10,
        decimal=','
    )

    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)

    df_residents = pd.read_csv(
        os.path.join(os.getcwd(), 'datasets', 'plz_einwohner.csv'), delimiter=','
    )
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
# -----------------------------------------------------------------------------------------------------------------------

    #


if __name__ == "__main__":
    main()

