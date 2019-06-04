"use-strict"


mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'


var map = new mapboxgl.Map({
  // create a map variable 
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-122.4194, 37.7749],
  zoom: 11
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
      // add point layer to map 
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

  // event to activate sidebar on click 
  map.on('click', 'art-point', function (evt) {
     
     map.getCanvas().style.cursor = 'pointer';

     var coordinates = evt.features[0].geometry.coordinates;
     var art_id = evt.features[0].properties.art_id; 

     $('#Sidebar').css("width", "25%");
  });

  // popup variable 
  var popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
   });

  // event to show popup on mouse hover 
  map.on('mouseenter', 'art-point', function (evt) {

    map.getCanvas().style.cursor = 'pointer';

    var coordinates = evt.features[0].geometry.coordinates;
    var source = evt.features[0].properties.source;

    popup.setLngLat(coordinates)
      .setHTML(source)
      .addTo(map);

  });

  // handle closing sidebar and popup on click TODO: why is tooltip not closing
  $('#closebtn').on('click', function (evt) {
     $('#Sidebar').css("width", "0");
  });

  // show the art hint in the sidebar 
  function showArtInfo(response) {

    $('#hint').html(response.hint);
    $('#title').html(response.title);
    $('#artist').html(response.artist);
  }

  function handleInfoEvent(evt) {
    evt.preventDefault();

    const artId = evt.features[0].properties.art_id
    $.get('/art/' + artId, showArtInfo);
  }

  map.on('click', 'art-point', handleInfoEvent);

  // go to log page from side bar 
  function showLogForm() {
    
    $('#log-info').append('<form action="/log/<art_id>" id="log-form" methods="POST"><input type="file" name="image"></input><br><input type="text" name="comment"></input><br><input type="submit" value="submit"></form>');
  }

  $('#log').on('click', showLogForm);

  function showInfoPage() {
    console.log('HELLOOOOOOOOOOOO');
    $('#log-info').replaceWith('<ul><p>PHOTO COMMENT</p></ul>');
  }

  $('#info').on('click', showInfoPage);

  // function submitArtLog(evt) {
  //   evt.preventDefualt();

  //   const artId = evt.features[0].properties.art_id
  //   console.log(artId)

  //   const formData = {
  //     image: $('#image').val(),
  //     comment: $('#comment').val()
  //   }

  //   console.log('GET /info for log');

  //   $.get('/log/' + artId, formData)
  // }

  const nav = new mapboxgl.NavigationControl();
  map.addControl(nav, 'bottom-right');

