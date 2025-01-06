from flask import Flask, request, url_for, render_template, redirect
import pandas as pd
from pyproj import Proj, transform

# Define the UTM Zone 37S (EPSG:32737) projection
utm_proj = Proj(proj="utm", zone=37, south=True, ellps="WGS84", datum="WGS84")

# Define the WGS 84 (EPSG:4326) projection
wgs84_proj = Proj(proj="latlong", datum="WGS84")


app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template('index.html')

@app.route("/dashboard", methods=["GET"])
def dashboard():

    if request == "GET":
       
        return render_template("dashboard.html")
    
    data = pd.read_csv('static/ground data.csv')
    random_row = data.sample(n=1).iloc[0]

    species = random_row['Species name (scientific)']
    coordinates = (random_row['UTM_Easting'], random_row['UTM_Northing'])
    height = random_row['Tree Height']
    biomass = random_row['Biomass']
    biomass = round(biomass, 2)

    utm_x, utm_y = coordinates[0], coordinates[1]
    lon, lat = transform(utm_proj, wgs84_proj, utm_x, utm_y)

    print(f"Converted Coordinates: Longitude = {lon}, Latitude = {lat}")

    return render_template("dashboard.html", species=species, coordinates=coordinates, height=height, biomass=biomass, lon=lon, lat=lat)

@app.route('/about', methods=["GET", "POST"])
def about():

    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)