"use-strict"


mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'


var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-122.4194, 37.7749],
  zoom: 11
  });

map.on('load', function () {
  if (map.loaded()) {
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
      "heatmap-radius": [
        "interpolate",
        ["linear"],
        ["zoom"],
        0, 2,
        9, 20
        ],
      'heatmap-opacity': {
        default: 1,
        stops: [
          [11, 1],
          [14, 0]
          ]
          },
        }
      }, 'waterway-label');
    
    map.addLayer({
        id: 'art-point',
        type: 'circle',
        source: 'artworks',
        paint: {
          'circle-radius': 5,
          'circle-color': {
            property: 'source',
            type: 'categorical',
            stops: [
              ['civic', '#fbb03b'],
              ['user', '#214BCC'],
              ['public_oneper', '#e55e5e']
            ]
          },
          'circle-opacity': {
            stops: [
              [11, 0],
              [15, 1]
            ]
          }
        }
    }, 'waterway-label');

    }});

  map.on('click', 'art-point', function (evt) {
     
     map.getCanvas().style.cursor = 'pointer';

     var coordinates = evt.features[0].geometry.coordinates;
     console.log(coordinates)
     var art_id = evt.features[0].properties.art_id; 
     console.log(art_id)

     $('#mySidebar').css("width", "25%");
     console.log("MADE IT HERE")
     $('#map').css("marginLeft", "0");
     console.log("MADE IT HERE")


  });

  $('#closebtn').on('click', function (evt) {
     $('#mySidebar').css("width", "0");
     console.log("MADE IT HERE")
     $('#map').css("marginLeft", "0");
     console.log("MADE IT HERE")
  })

  // var popup = new mapboxgl.Popup({
  //   closeButton: false,
  //   closeOnClick: true
  //  });

  // map.on('mouseenter', 'art-point', function (evt) {

  //   map.getCanvas().style.cursor = 'pointer';

  //   var coordinates = evt.features[0].geometry.coordinates;
  //   // var source = evt.features[0].properties.source;
  //   var str = "Info";
  //   // var link = str.link(`/art/${evt.features[0].properties.art_id}`);

  //   str.on('click', function (evt) {
  //     $("#mySidebar").style.width = "250px";
  //     $("#map").style.marginLeft = "250px";
  //   });

  //   function closeNav() {
  //     $("#mySidebar").style.width = "0";
  //     $("#map").style.marginLeft= "0";
  //   }


  //   popup.setLngLat(coordinates)
  //     // .setHTML(source)
  //     .setHTML(str)
  //     .addTo(map);


  // });

  map.addControl(new mapboxgl.NavigationControl());
