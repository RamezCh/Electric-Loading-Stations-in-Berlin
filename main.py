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
    ## Gap Analysis: EV Charging Infrastructure in Berlin
    This project employs a bivariate spatial analysis to compare **Residential Population Density (Demand)** against **Public Charging Station Distribution (Supply)** across Berlin ZIP codes.
    
    **The Core Finding:**
    Berlin exhibits a critical **"Structural Mismatch"** in its infrastructure rollout.
    1.  **The Center (Mitte)** is well-served.
    2.  **The Eastern Corridor (Biesdorf)** is statistically saturated, likely due to commercial transit hubs rather than residential need.
    3.  **The High-Density Residential Belt (The Ring)** where the need is highest due to a lack of private parking is significantly underserved.
    
    ---
    
    ### 2. Methodology: Demand vs. Supply
    
    #### A. Demand Layer (Population Density)
    * **Metric:** Residents per ZIP code.
    * **High Density (Red/Orange):** Concentrated in the "Wilhelminian Ring" (Neukölln, Kreuzberg, Friedrichshain, Prenzlauer Berg, Wedding, Charlottenburg) and high-rise estates in the East (Marzahn/Hellersdorf).
    * **Implication:** Areas with high vertical density (Multi-Dwelling Units or MDUs) lack private driveways. **Residents here are 100% dependent on public street charging.**
    
    #### B. Supply Layer (Charging Stations)
    * **Metric:** Count of public charging points per ZIP code.
    * **Distribution:** Heavily skewed towards the city center (Mitte) and specific commercial arteries (B1/B5 in Biesdorf).
    * **Deficit:** The majority of residential districts show "Yellow" (Low Supply), creating a mismatch in areas where EV adoption is stifled by infrastructure anxiety.
    
    ---
    
    ### 3. Priority 1: The "Crisis Belt" (Inner City Ring)
    *Definition: High Population Density (>20k) + Low Infrastructure (<10 stations).*
    
    These districts represent the highest ROI (Return on Investment) for new stations because the gap between potential users and available plugs is widest. Residents here generally cannot install Wallboxes.
    
    * **Neukölln (North):** (PLZ: 12043, 12045, 12047)
        * *Status:* Extreme population density; almost zero public infrastructure coverage.
        * *Action:* **Critical Priority.**
    * **Wedding & Moabit:** (PLZ: 13347, 13353, 10551)
        * *Status:* Densely populated working-class districts. Currently acting as "charging deserts."
        * *Action:* **Critical Priority.**
    * **Charlottenburg-Wilmersdorf:** (PLZ: 10585, 10623)
        * *Status:* Wealthier demographic with higher likelihood of EV ownership, yet the map shows significant infrastructure gaps compared to neighboring Mitte.
        * *Action:* **High Priority.**
    * **Friedrichshain:** (PLZ: 10245, 10247)
        * *Status:* High density of young professionals (early adopters), currently underserved.
    
    ---
    
    ### 4. Priority 2: The Eastern Dichotomy (The Biesdorf Anomaly)
    *Definition: A spatial mismatch where supply is located in commercial zones, ignoring residential zones.*
    
    This area highlights a flaw in simple data interpretation:
    * **The Anomaly (Biesdorf - 12683):**
        * *Observation:* Shows **Red (High Supply)**.
        * *Reality:* This is a **Transit/Commercial Hub** along the B1/B5 highway (Retail parks, Hardware stores, Dealerships). It serves commuters and shoppers, **not residents**.
    * **The Opportunity (Marzahn - 12681, 12685):**
        * *Observation:* Just north of Biesdorf, the map is **Yellow (Low Supply)**.
        * *Reality:* This area contains high-density *Plattenbau* (high-rise) estates. Residents here have no garages and cannot use the "Shopper Chargers" in Biesdorf for overnight parking.
        * *Action:* Shift focus from the Biesdorf commercial strip to the **Marzahn residential interior**.
    
    ---
    
    ### 5. Priority 3: Outer District Centers
    *Definition: Localized density spikes in the suburbs.*
    
    * **Spandau (Center - 13581):** A "city within a city" that is currently isolated from the charging network.
    * **Steglitz:** High residential density with minimal curbside options.
    
    ---
    
    ### 6. Low Priority / No Action Required
    
    #### A. Saturated Zones
    * **Mitte (10115, 10117):**
        * Supply is high and proportional to commercial activity. No urgent expansion needed relative to other districts.
    
    #### B. Self-Sufficient Zones (Suburbs)
    * **Wannsee, Gatow, Frohnau, Mahlsdorf:**
        * *Status:* Low population density (Green) and Low Supply (Yellow).
        * *Reasoning:* Predominantly Single-Family Homes (SFH). Residents here install private chargers in their driveways. Public infrastructure here has a very low utilization rate and is not a priority.
    
    ---
    
    ### 7. Strategic Recommendations
    
    To maximize utilization rates and support the mobility transition, the rollout strategy must pivot:
    
    1.  **Stop optimizing for "Coverage Maps":** Placing chargers in commercial strips (like Biesdorf) makes the map look good but doesn't help residents.
    2.  **Target "Overnight" Zones:** Focus entirely on **Neukölln**, **Wedding**, and **Marzahn North**. These are the areas where EV adoption is physically impossible without public street infrastructure.
    3.  **Data Filtering:** For future analysis, filter out "High Power Chargers" (HPC) at gas stations to get a true picture of "Residential Neighborhood Charging" availability.
    """)
    st.markdown("_")

