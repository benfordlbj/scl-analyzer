import xml.etree.ElementTree as ET
from datetime import datetime
import plotly.express as px
import pandas as pd

xml_source = 'data/scl_electric_60_Minute_05-01-2026_05-14-2026.xml'

def parse_and_plot_electricity(xml_source, is_file=True):
    # Define common ESPI/Atom namespaces
    ns = {
        'atom': 'http://w3.org',
        'espi': 'http://naesb.org/espi'
    }

    # 1. Parse XML structure
    if is_file:
        tree = ET.parse(xml_source)
        root = tree.getroot()
    else:
        root = ET.fromstring(xml_source)

    timestamps = []
    consumption = []

    # 2. Extract timestamp and usage value tags
    for block in root.findall('.//espi:IntervalBlock', ns):
        for reading in block.findall('.//espi:IntervalReading', ns):
            try:
                start_element = reading.find('.//espi:start', ns)
                value_element = reading.find('.//espi:value', ns)

                if start_element is not None and value_element is not None:
                    # Convert Unix epoch timestamp to datetime object
                    epoch_time = int(start_element.text)
                    dt = datetime.fromtimestamp(epoch_time)

                    timestamps.append(dt)
                    consumption.append(float(value_element.text))
            except (ValueError, TypeError) as e:
                print(f"Skipping malformed row: {e}")
                continue

    # 3. Structure data into a pandas DataFrame
    df = pd.DataFrame({"Timestamp": timestamps, "Usage_kWh": consumption})
    df = df.sort_values(by="Timestamp")
    df['Usage_kWh'] = df['Usage_kWh'].div(1000000)

    fig = px.line(df, x='Timestamp', y='Usage_kWh',
                  labels={
                     "Timestamp": "Timestamp",
                     "Usage_kWh": "Usage (kWh)"
                  }, title='Ben and Naomi\'s Electricity Use', template="plotly_white")

    fig.show()

# To run from a local XML file, use: parse_and_plot_electricity('your_file.xml', is_file=True)
parse_and_plot_electricity(xml_source, is_file=True)