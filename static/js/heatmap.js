"use-strict"


function renderMap() {

  mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'


    var map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/light-v10',
      center: [-122.4194, 37.7749],
      zoom: 11
      });

    map.on('load', function () {
      // add a geojson point source for artworks 
      map.addSource('artworks', {
        type: 'geojson',
        data: '/artworks.geojson'
      });
      
      // add layer for heat map 
      map.addLayer({
        id: 'art-heat',
        type: 'heatmap',
        source: 'artworks',
        maxzoom: 15,
        paint: {
          'heatmap-intensity': {
            stops: [
            [11, 1],
            [15, 3]
          ]
        },
        'heatmap-color': [
        'interpolate',
          ['linear'],
          ['heatmap-density'],
            0, "rgba(33,102,172,0)",
            0.2, "rgb(103,169,207)",
            0.4, "rgb(209,229,240)",
            0.6, "rgb(253,219,199)",
            0.8, "rgb(239,138,98)"
          ],
        'heatmap-radius': {
            stops: [
            [11, 15],
            [15, 20]
          ]
        },
        'heatmap-opacity': {
          default: 1,
          stops: [
            [14, 1],
            [15, 0]
            ]
            },
          }
        }, 'waterway-label');

      map.addLayer({
        id: 'art-point',
        type: 'circle',
        source: 'artworks',
        minzoom: 14,
        paint: {
          'circle-radius': {
            property: 'source',
            type: 'exponential',
            stops: [
              [{ zoom: 15, value: 1 }, 5],
              [{ zoom: 15, value: 62 }, 10],
              [{ zoom: 22, value: 1 }, 20],
              [{ zoom: 22, value: 62 }, 50],
            ]
          },
            'circle-color': {
              property: 'source',
              type: 'exponential',
              stops: [
                [0, 'rgba(236,222,239,0)'],
                [10, 'rgb(236,222,239)'],
                [20, 'rgb(208,209,230)'],
                [30, 'rgb(166,189,219)'],
                [40, 'rgb(103,169,207)'],
                [50, 'rgb(28,144,153)'],
                [60, 'rgb(1,108,89)']
              ]
            },
            'circle-stroke-color': 'white',
            'circle-stroke-width': 1,
            'circle-opacity': {
              stops: [
                [14, 0],
                [15, 1]
              ]
            }
          }
          }, 'waterway-label');

    });

    var popup = new mapboxgl.Popup({
      closeButton: false,
      closeOnClick: false
     });

    map.on('mouseenter', 'art-point', function (evt) {

      map.getCanvas().style.cursor = 'pointer';

      var coordinates = evt.features[0].geometry.coordinates;
      var source = evt.features[0].properties.source;

      // while (Math.abs(evt.lnglat.lng - coordinates[0]) > 180) {
      //   coordinates[0] += evt.lngLat.lng > coordinates[0] ? 360 : -360;
      // }

      popup.setLngLat(coordinates)
        .setHTML(source)
        .addTo(map);

    });

    map.addControl(new mapboxgl.NavigationControl());
  }

$('#heatmap').on('click', renderMap)