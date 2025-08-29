"""Streamlit app for visualising Belgian real‑estate agents data.

This application reads a CSV file containing details about leading real‑estate
agencies in Belgium and exposes three interactive visualisations: a table,
bar chart and geographical map with connectors. The map centres on Brussels
and draws a line from the city centre to each agency's head office. The
purpose is to give a clear, concise overview of where these companies
operate and how their latest profits compare.

To run the application locally, first install the requirements found in
``requirements.txt`` and then launch with ``streamlit run app.py``.
"""

import pathlib
from typing import Dict, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
import folium


def load_data(csv_path: str) -> pd.DataFrame:
    """Load the real‑estate agents dataset and enrich it with numeric profit.

    Args:
        csv_path: Path to the CSV file containing the agents data.

    Returns:
        DataFrame with an additional 'Profit' column parsed from the
        'Latest profit after tax (€)' column.
    """
    df = pd.read_csv(csv_path)
    # Clean the profit column by removing currency symbols, commas and spaces
    cleaned = (
        df["Latest profit after tax (€)"].astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.strip()
    )
    df["Profit"] = pd.to_numeric(cleaned, errors="coerce")
    return df


def get_coordinates() -> Dict[str, Tuple[float, float]]:
    """Return approximate latitude/longitude for each locality in the dataset.

    These coordinates were manually derived using public geographic
    information to serve as a basis for the folium map. If more precise
    geocoding is required, consider integrating an API such as Nominatim.
    """
    return {
        "Waterloo": (50.7219, 4.3997),
        "Brussels": (50.8466, 4.3528),
        "Strombeek-Bever": (50.9050, 4.3681),
        "Brussels (Uccle)": (50.7997, 4.3476),
        "Sint-Niklaas": (51.1642, 4.1439),
        "Brussels (Ixelles)": (50.8287, 4.3676),
        "Brussels (1000)": (50.8466, 4.3528),
    }


def enrich_with_coords(df: pd.DataFrame) -> pd.DataFrame:
    """Append latitude and longitude to the dataframe based on locality.

    Args:
        df: DataFrame containing a 'Locality' column.

    Returns:
        DataFrame with new 'Latitude' and 'Longitude' columns.
    """
    coords = get_coordinates()
    latitudes = []
    longitudes = []
    for loc in df["Locality"]:
        # If exact match not found, attempt to map to Brussels by default
        lat, lon = coords.get(loc, coords.get("Brussels"))
        latitudes.append(lat)
        longitudes.append(lon)
    df = df.copy()
    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    return df


def build_bar_chart(df: pd.DataFrame) -> None:
    """Render a bar chart of latest profits using Plotly within Streamlit.

    Args:
        df: DataFrame with 'Name' and 'Profit' columns.
    """
    bar = px.bar(
        df,
        x="Name",
        y="Profit",
        color="Profit",
        labels={"Profit": "Profit (€)"},
        title="Latest Profit After Tax by Company",
    )
    bar.update_layout(xaxis_title="Company", yaxis_title="Profit (€)")
    st.plotly_chart(bar, use_container_width=True)


def build_map(df: pd.DataFrame) -> None:
    """Render a folium map with markers and connectors for each agent.

    Args:
        df: DataFrame with 'Name', 'Address', 'Latitude' and 'Longitude'.
    """
    # Centre of Belgium/Brussels for the map
    center = (50.8466, 4.3528)
    m = folium.Map(location=center, zoom_start=8)
    # Add marker and line for each company
    for _, row in df.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]
        popup = f"<b>{row['Name']}</b><br>{row['Address']}"
        folium.Marker([lat, lon], popup=popup).add_to(m)
        # Draw connector line from centre to company location
        folium.PolyLine(locations=[center, (lat, lon)], color="blue", weight=1).add_to(m)
    folium_static(m, width=700, height=500)


def main() -> None:
    """Main entry point for the Streamlit app."""
    st.set_page_config(page_title="Belgian Real‑estate Agents", layout="wide")
    st.title("Belgian Real‑estate Agents: Data Overview")
    # Determine CSV path relative to this file. The dataset may reside either
    # alongside this script or one directory above (depending on how the
    # repository is organised). We try the local directory first and fall
    # back to the parent directory if not found.
    script_dir = pathlib.Path(__file__).resolve().parent
    local_csv = script_dir / "belgian_real_estate_agents.csv"
    parent_csv = script_dir.parent / "belgian_real_estate_agents.csv"
    csv_path = local_csv if local_csv.exists() else parent_csv
    df = load_data(str(csv_path))
    df = enrich_with_coords(df)
    # Show table
    st.header("Data Table")
    st.dataframe(df.drop(columns=["Latitude", "Longitude"]))
    # Show bar chart
    st.header("Latest Profit After Tax (Euro)")
    build_bar_chart(df)
    # Show map
    st.header("Map of Agents with Connectors")
    build_map(df)


if __name__ == "__main__":
    main()