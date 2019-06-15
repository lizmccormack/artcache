'user-strict'

let placeSearch, autocomplete; 

let componentForm = {
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

  // populate address fields 
  autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
  let place = autocomplete.getPlace();
  console.log(place)

  for (let component in componentForm) {
    document.getElementById(component).value = '';
    document.getElementById(component).disabled = false; 
  }

  for (let i = 0; i < place.address_components.length; i++) {
    let addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
       let val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val; 
        }
    }
}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      let geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      console.log(geolocation)
      let circle = new google.maps.Circle(
          {center: geolocation, radius: position.coords.accuracy});
      autocomplete.setBounds(circle.getBounds());
    });
  }
}
    