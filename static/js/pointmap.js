"use-strict"


function renderMap() {

  mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'

  var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-122.4300, 37.7600],
  zoom: 12
  });

  map.on('load', function () {
    // add a geojson point source for artworks 
    map.addSource('artworks', {
      type: 'geojson',
      data: '/artworks.geojson'
    });

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
          }
        }
    });

    var popup = new mapboxgl.Popup({
      closeButton: false,
      closeOnClick: false
     });

    map.on('mouseenter', 'art-point', function (evt) {

      map.getCanvas().style.cursor = 'pointer';

      var coordinates = evt.features[0].geometry.coordinates;
      var str = "Log";
      var source = (evt.features[0].properties.source, str.link(`/art/${evt.features[0].properties.art_id}`));

      // var link = str.link(`/log/${evt.features[0].properties.art_id}`);

      popup.setLngLat(coordinates)
        .setHTML(source)
        .addTo(map);

    });

    map.addControl(new mapboxgl.NavigationControl());

})}


$('#pointmap').on('click', renderMap);