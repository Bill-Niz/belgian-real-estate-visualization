# Belgian Real‑Estate Agents Visualisation

This repository contains a curated dataset of leading real‑estate agencies
operating in Belgium and a small web application to explore the data
interactively. The dataset includes details such as company names,
addresses, contact information, VAT numbers and their most recent
profits. The application uses [Streamlit](https://streamlit.io/) for
its user interface, Plotly for charting, and Folium for mapping.

## Dataset

The `belgian_real_estate_agents.csv` file (located one directory up)
captures publicly available information about nine prominent agencies.
Fields include:

- **Name** – official company name.
- **Address** – head office location.
- **Social media** – list of supported social platforms.
- **Email** – general contact address.
- **Zip code** and **Locality** – used for geographic plotting.
- **Company size** – approximate number of employees or FTE.
- **TVA number** – Belgian VAT number.
- **Latest profit after tax (€)** – most recent profit/loss, as published in
  financial statements.

## Running the App

1. **Install dependencies**

   Use a virtual environment and install packages from `requirements.txt`:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Launch the application**

   From the `real_estate_visualization` directory, run:

   ```bash
   streamlit run app.py
   ```

3. **Explore**

   The web interface will display:

   - A searchable table of all agencies.
   - A bar chart comparing their latest profits.
   - An interactive map centred on Brussels with lines connecting the city centre to each agency’s head office.

## Notes

* Coordinates used for the map are approximate and derived from public
  geographic information; they are sufficient for visualisation but not
  for navigation.
* If you plan to add more agencies, update the CSV file accordingly and
  restart the app.
* For accurate geocoding consider integrating an API such as
  [Nominatim](https://nominatim.org/).