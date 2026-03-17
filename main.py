from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations.columns = stations.columns.str.strip()
stations = stations[["STAID", "STANAME"]]

@app.route("/")
def home():
    return render_template(
        "home.html", data=stations.to_html()
    )


@app.route("/api/v1/<station>")
def station_all_data(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/<station>/day/<date>")
def station_data_at_date(station, date):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df["TG"] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df["TG"] = df["TG"] / 10
    temperature = df.loc[df["    DATE"] == date]["TG"].squeeze()
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/<station>/year/<year>")
def station_data_at_year(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df[df["    DATE"].dt.year == int(year)].to_dict(orient="records")
    return result

if __name__ == "__main__":
    app.run(debug=True)