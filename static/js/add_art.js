'user-strict'

var placeSearch, autocomplete; 

var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initAutocomplete() {
  // set the autocomplete object and only allow locations with geocode 
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: ['geocode']});

  // restrics return data to address_component
  autocomplete.setFields(['address_component']);

  // populate address fields when the user selects from the dropdown 
  autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
  var place = autocomplete.getPlace();
  console.log(place)

  for (var component in componentForm) {
    document.getElementById(component).value = '';
    document.getElementById(component).disabled = false; 
  }

  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
       var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val; 
        }
    }
}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      console.log(geolocation)
      var circle = new google.maps.Circle(
          {center: geolocation, radius: position.coords.accuracy});
      autocomplete.setBounds(circle.getBounds());
    });
  }
}
    