"use-strict"


mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'


let map = new mapboxgl.Map({
  // create a map variable 
  container: 'map',
  style: 'mapbox://styles/lizmccormack/cjwtkxume7k901cpadxxgdlm1/draft',
  center: [-122.4450, 37.7600],
  zoom: 11.5,
  // bearing: 27,
  // pitch: 45
  });

map.on('load', function () {
  if (map.loaded()) {

    map.addSource('artworks', {
      // add a geojson point source for artworks 
      type: 'geojson',
      data: '/artworks.json'
    });
    
    
    map.addLayer({
      // add layer for heat map 
      id: 'art-heat',
      type: 'heatmap',
      source: 'artworks',
      maxzoom: 12,
      paint: {
        'heatmap-intensity': {
          stops: [
          [10, 1],
          [12, 3]
        ]
      },
      'heatmap-color': [
      'interpolate',
        ['linear'],
        ['heatmap-density'],
          0, "rgba(0,0,255,0)",
          0.2, "#ffffb2",
          0.4, "#feb24c",
          0.6, "#fd8d3c",
          0.8, "#e41b1e"
        ], 
      "heatmap-radius": [
        "interpolate",
        ["linear"],
        ["zoom"],
        0, 2,
        12, 20
        ],
      'heatmap-opacity': {
        default: 1,
        stops: [
          [11, 1],
          [12, 0]
          ]
          },
        }
      });
    
    map.addLayer({
      // add point layer to map 
        id: 'art-point',
        type: 'circle',
        source: 'artworks',
        minzoom: 12,
        paint: {
          'circle-radius': 4,
          'circle-color': {
            property: 'source',
            type: 'categorical',
            stops: [
              ['civic', '#FF3C00'],
              ['user', '#3e7ec1'],
              ['public_oneper', '#fbda42']
            ]
          },
          'circle-opacity': {
            stops: [
              [11, 0],
              [12, 1]
            ]
          }
        }
    });

    }});

  // event to activate sidebar on click 
  map.on('click', 'art-point', function (evt) {
     
     map.getCanvas().style.cursor = 'pointer';

     let coordinates = evt.features[0].geometry.coordinates;
     let art_id = evt.features[0].properties.art_id; 

     $('#Sidebar').css("width", "25%");
  });

// popup variable 
let popup = new mapboxgl.Popup({
  closeButton: true,
  closeOnClick: false
});

// event to show popup on mouse hover 
map.on('mouseenter', 'art-point', function (evt) {

  map.getCanvas().style.cursor = 'pointer';

  let coordinates = evt.features[0].geometry.coordinates;
  let title = evt.features[0].properties.title;
  let hint = evt.features[0].properties.hint;

  popup.setLngLat(coordinates)
    .setHTML('<h7><strong>' + title + '</strong></h7><br><div>Hint: ' + hint + '</div>')
    .addTo(map);

});

const legend = $('#art-legend');
const legendDisplaySettings = legend[0].style.displaysettings
map.on('zoom', function() {
  if (map.getZoom() > 12) {
    legend[0].style.display = 'block';
  } else {
    legend[0].style.display = 'none';
  }
}); 


const nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'bottom-right');

