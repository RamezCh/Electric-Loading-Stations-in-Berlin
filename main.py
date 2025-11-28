# -----------------------------------------------------------------------------
import os
currentWorkingDirectory =  os.getcwd()
print("Current working directory\n" + currentWorkingDirectory)
import streamlit                     as st
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
    # -------------------------------------------------------------------------
    # TASK 7: ANALYSIS & INTERPRETATION
    # -------------------------------------------------------------------------
    st.markdown("---")  # Trennlinie
    st.header("7) Analysis of Demand")

    st.markdown("""
    By comparing the *Residents* layer with the *Charging_Stations* layer, we can identify clear patterns regarding the demand for new infrastructure:

    ### 1. High Demand in Residential High-Rises (Hotspots)
    There is a significant mismatch in densely populated outer districts, such as *Marzahn-Hellersdorf, **Lichtenberg, and southern **Neukölln* (e.g., Gropiusstadt).
    * *Observation:* These areas appear *dark red* in the Residents map (high density) but remain *yellow/green* in the Charging Stations map (low supply).
    * *Reasoning:* Residents in these apartment complexes usually lack private garages. They rely entirely on public charging infrastructure ("lantern parkers").

    ### 2. The "Suburban Effect"
    In districts like *Steglitz-Zehlendorf* or *Reinickendorf*, the density of public chargers is also low, but the urgency is different.
    * *Reasoning:* These areas are characterized by single-family houses. EV owners here typically install *private wallboxes* on their driveways. Therefore, the demand for public stations is naturally lower than in the city center or high-rise areas.

    ### Conclusion & Recommendation
    Future infrastructure investments should prioritize *densely populated residential areas* where private charging is not possible. The data suggests a supply gap in the eastern outer districts compared to the well-supplied city center.
    """)
    st.markdown("_")

