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

    map.addLayer({
        id: 'art-point',
        type: 'circle',
        source: 'artworks'
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


$('#pointmap').on('click', renderMap);