"use-strict"

mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'

// create map variable
var map_tour = new mapboxgl.Map({
  container: 'map-tour',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-122.4194, 37.7749],
  zoom: 14,
  bearing: 27,
  pitch: 45

});

// sidebar with information and pictures 
$('#features').css("width", "25%");


// create variables for the different sites 
const sites = {
  'site1': {
    bearing: 27,
    center: [-122.419490, 37.763060],
    zoom: 15.5,
    pitch: 20
  },
  'site2': {
    duration: 6000,
    center: [-122.422620, 37.761420],
    bearing: 150,
    zoom: 15,
    pitch: 0
  },
  'site3': {
    bearing: 90,
    center: [-122.473640, 37.756120],
    zoom: 13,
    speed: 0.6,
    pitch: 40
  },
  'site4': {
    bearing: 90,
    center: [-122.510178, 37.769485],
    zoom: 12.3
  },
  'site5': {
    bearing: 45,
    center: [-122.492630, 37.785170],
    zoom: 15.3,
    pitch: 20,
    speed: 0.5
  }
};

// set active site when scrolling through side bar 
$('#features').on('scroll', function() {

  const siteNames = Object.keys(sites);
  console.log(sites)
    for (var i = 0; i < siteNames.length; i++) {
      const siteName = siteNames[i];
      if (isElementOnScreen(siteName)) {
      setActiveSite(siteName);
    break;
    }
  }
});

// set active site and change location based on active site  
var activeSiteName = 'site1';
function setActiveSite(siteName) {
  if (siteName === activeSiteName) return;

  map_tour.flyTo(sites[siteName]);

  document.getElementById(siteName).setAttribute('class', 'active');
  document.getElementById(activeSiteName).setAttribute('class', '');

  activeSiteName = siteName;
}
 
//set window box to item on screen  
function isElementOnScreen(id) {
    var element = document.getElementById(id);
    var bounds = element.getBoundingClientRect();
    return bounds.top < window.innerHeight && bounds.bottom > 0;
}