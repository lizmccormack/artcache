"use-strict"


mapboxgl.accessToken = 'pk.eyJ1IjoibGl6bWNjb3JtYWNrIiwiYSI6ImNqdndyNWJzNjBwYW40NHFkZGpzdTZ2amwifQ.vkULiOOFr4KqS7o2_enuyA'

var map_tour = new mapboxgl.Map({
  container: 'map-tour',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-122.4194, 37.7749],
  zoom: 14,
  bearing: 27,
  pitch: 45

});

$('#features').css("width", "25%");


var chapters = {
  'site1': {
    bearing: 27,
    center: [-122.4666711, 37.7703537],
    zoom: 15.5,
    pitch: 20
  },
  'site2': {
    duration: 6000,
    center: [-122.419491, 37.74406],
    bearing: 150,
    zoom: 15,
    pitch: 0
  },
  'site3': {
    bearing: 90,
    center: [-122.421886, 37.764766],
    zoom: 13,
    speed: 0.6,
    pitch: 40
  },
  'site4': {
    bearing: 90,
    center: [-122.4331353 , 37.8021249],
    zoom: 12.3
  },
  'site5': {
    bearing: 45,
    center: [-122.42028, 37.764154],
    zoom: 15.3,
    pitch: 20,
    speed: 0.5
  },
  'site6': {
    bearing: 180,
    center: [-122.422523, 37.77818],
    zoom: 12.3
  },
  'site7': {
    bearing: 90,
    center: [-122.38366, 37.62207],
    zoom: 17.3,
    pitch: 40
  },
  'site8': {
    bearing: 90,
    center: [-122.38366, 37.62207],
    zoom: 14.3,
    pitch: 20
  }
};

$('#features').on('scroll', function() {

  var chapterNames = Object.keys(chapters);
  console.log(chapters)
    for (var i = 0; i < chapterNames.length; i++) {
      var chapterName = chapterNames[i];
      if (isElementOnScreen(chapterName)) {
      setActiveChapter(chapterName);
    break;
    }
  }
});
 
var activeChapterName = 'site1';
function setActiveChapter(chapterName) {
  if (chapterName === activeChapterName) return;

  map_tour.flyTo(chapters[chapterName]);

  document.getElementById(chapterName).setAttribute('class', 'active');
  document.getElementById(activeChapterName).setAttribute('class', '');

  activeChapterName = chapterName;
}
 
function isElementOnScreen(id) {
    var element = document.getElementById(id);
    var bounds = element.getBoundingClientRect();
    return bounds.top < window.innerHeight && bounds.bottom > 0;
}