import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { Map, Marker, Popup, } from "react-leaflet";
import { Icon } from "leaflet";
import * as ReactLeaflet from "react-leaflet"
import ReactDOM from 'react-dom';
import * as forestJson from "./data/ForestJson.json"
import * as carbonJSON from "./data/carbonFeaturesCollection.json"
import * as carbobData from "./data/carbonFeaturesCollecJson.json"
import axios from "axios";
import { AxiosProvider, Request, Get, Delete, Head, Post, Put, Patch, withAxios } from 'react-axios'


const forest = forestJson.features
console.log('forest at 0 : ', forestJson.features[0])
console.log('forest at 1 : ', forestJson.features[1])
// const data = { type: "FeatureCollection", features: carbonJSON.default };
// const newdata = data

let forest_SHAPE_Area = null;

// const newdata = carbobData.features //change back to data

const { Map: LeafletMap, Polygon, Pane, MapLayer, TileLayer, GeoJSON, LayerGroup, LayersControl, FeatureGroup, CheckBox } = ReactLeaflet;

const { BaseLayer, Overlay } = LayersControl


const polygon = [[32, -88], [32, -79], [24, -79], [24, -88], [32, -88]]

// variable declaration for carbon
let mapRef;
const COLOR_0 = "#800026";
const COLOR_9 = "#BD0026";
const COLOR_10 = "#E31A1C";
const COLOR_11 = "#FC4E2A";
const COLOR_12 = "#FD8D3C";
const COLOR_13 = "#FEB24C";
const COLOR_14 = "#FED976";
const COLOR_15 = '#FFEDA0';


//function returning Carbon colors
function getColor(d) {
  return d > 15 ? '#800026' :
    d > 14 ? '#BD0026' :
      d > 13 ? '#E31A1C' :
        d > 12 ? '#FC4E2A' :
          d > 11 ? '#FD8D3C' :
            d > 10 ? '#FEB24C' :
              d > 9 ? '#FED976' :
                '#FFEDA0';
}

function getColorForest(d) {
  return d > 15 ? '#005824' :
    d > 14 ? '#238b45' :
      d > 13 ? '#41ae76' :
        d > 12 ? '#66c2a4' :
          d > 11 ? '#99d8c9' :
            d > 10 ? '#ccece6' :
              d > 9 ? '#edf8fb' :
                '#f7fcfd';
}

//coloring the features of carbon
function style(feature) {
  return {
    fillColor: getColor(feature.properties.carbon),
    weight: 1,
    opacity: 1,
    color: "white",
    dashArray: "3",
    fillOpacity: 0.8
  };
}

function styleForest(feature) {
  return {
    fillColor: getColorForest(feature.properties.PROCLAIMEDFORESTID),
    weight: 1,
    opacity: 1,
    color: "white",
    dashArray: "3",
    fillOpacity: 0.8
  };
}



function zoomToFeature(e) {
  mapRef.fitBounds(e.target.getBounds());
}

function App() {
  /////// Getting Data from Flask
  const [newdata, setCarbonData] = useState(); //setting the data to the data variable

  useEffect(() => {
    console.log("here...")
    fetch("/map").then(response => // returns featureCollection for carbon
      response.json().then(flaskdata => {
        setCarbonData(flaskdata);
        // console.log("carbon data...", flaskdata);
      })
    );
  }, []);


  const [forestNew, setForestData] = useState(); //setting the data to the data variable

  useEffect(() => {
    console.log("In forest function...")
    fetch("/forest").then(response => // returns featureCollection for carbon
      response.json().then(forestdata => {
        setForestData(forestdata.features);
        // forest_SHAPE_Area = forestdata.features[0].properties.SHAPE_Area
        // console.log("forestdata..... : ", forestdata.features[0].properties.SHAPE_Area)
      })
    );
  }, []);

  // for (let [key, value] of Object.entries(newdata)) {
  //   console.log("Carbon new ",`${key}: ${value}`);
  // }
  

  // Mapping code for base layer  
  const [selected, setSelected] = React.useState({});

  function highlightFeature(e) {
    var layer = e.target;
    const { name, carbon } = e.target.feature.properties;
    setSelected({
      province: `${name}`,
      count: carbon
    });
    layer.setStyle({
      weight: 2,
      color: "#DF1995",
      dashArray: "",
      fillOpacity: 1
    });
    if (1 == 1) {
      layer.bringToFront();
    }
  }

  //For Forest
  function highlightFeatureForest(e) {
    var layer = e.target;
    const { FORESTNAME, GIS_ACRES } = e.target.feature.properties;
    setSelected({
      provinceForest: `${FORESTNAME}`,
      countForest: GIS_ACRES
    });
    layer.setStyle({
      weight: 2,
      color: "#DF1995",
      dashArray: "",
      fillOpacity: 1
    });
    if (1 == 1) {
      layer.bringToFront();
    }
  }


  function resetHighlight(e) {
    setSelected({});
    e.target.setStyle(style(e.target.feature));
  }

  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
    });
  }

  //For Forest
  function onEachFeatureForest(feature, layer) {
    layer.on({
      mouseover: highlightFeatureForest,
      mouseout: resetHighlight,
      click: zoomToFeature
    });
  }

  // Function to calculate reduced carbon
  
  function  calcutaleReducedCarbon(){
    console.log("Forest area........",forest_SHAPE_Area);
  }


  return (
    <div className="panel">
      <div className="panel__map">
        <button
          onClick={() => {
            mapRef.flyToBounds([
              [36.2422994, -113.7487596],
              [36.1890359, -70.97282],
            ]);
          }}
          className="full-extent"
        />
        {!selected.province && (
          <div className="hover-info">Hover over an Area</div>
        )}
        {selected.province && (
          <div className="info">
            <h2>{selected.province}</h2>
            <span class="countCol"><h4>{selected.count}&nbsp;&nbsp;&nbsp; CO2/parts per billion</h4></span>
          </div>
        )}
        {/* for forest */}
        {selected.provinceForest && (
          <div className="info">
            <h2>{selected.provinceForest}</h2>
            <span class="countCol"><h4>{selected.countForest}&nbsp;&nbsp;&nbsp; acres</h4></span>
          </div>
        )}
        {selected.provinceForest && (
          <div className="info">
            <h2>{selected.provinceForest}</h2>
            <span class="countCol"><h4>{selected.countForest}&nbsp;&nbsp;&nbsp; acres</h4></span>
          </div>
        )}


        <div className="legend">
          <p class="colWh">Carbon Pollution</p>
          <div style={{ "--color": COLOR_10 }}>15+</div>
          <div style={{ "--color": COLOR_11 }}>13 - 14</div>
          <div style={{ "--color": COLOR_12 }}>12 - 13</div>
          <div style={{ "--color": COLOR_13 }}>11 - 12</div>
          <div style={{ "--color": COLOR_14 }}>10 - 11</div>
          <div style={{ "--color": COLOR_15 }}>0-10</div>
        </div>
        <LeafletMap
          style={{ width: "100%", height: "100%" }}
          zoom={1}
          zoomControl={false}
          //maxZoom={4}
          center={[37.8, -96]}
          whenReady={e => {
            mapRef = e.target;
            e.target.flyToBounds([
              [36.2422994, -113.7487596],
              [36.1890359, -70.97282],
            ]);
          }}
        >
          <LayersControl position="topright">
            <BaseLayer checked name="OpenStreetMap.Mapnik">
              <TileLayer
                attribution="Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
                url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
              />
            </BaseLayer>
            <BaseLayer name="OpenStreetMap.BlackAndWhite">
              <TileLayer
                attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"
              />
            </BaseLayer>
            <Overlay checked name="States Layer">
              <Pane name="countiesPane" style={{ zIndex: 500 }}>
                {newdata && (
                  <GeoJSON key='counties' data={newdata} style={style} onEachFeature={onEachFeature} />
                )}
              </Pane>
            </Overlay>
            <Overlay checked name="Forests Layer">
              <Pane name="forestsPane" style={{ zIndex: 501 }}>
                {forestNew && (
                  <GeoJSON key='forests' data={forestNew} style={styleForest} onEachFeature={onEachFeatureForest} />)}
              </Pane>
            </Overlay>
              
            {/* <Polygon positions={polygon} color='purple' /> */}
          </LayersControl>
        </LeafletMap>      </div>
    </div>
  );
}

export default App;

