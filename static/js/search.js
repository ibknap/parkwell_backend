var gmapGeocoder = new google.maps.Geocoder();
var gmapSearchInput = document.querySelector("#gmapSearchInput");
gmapAutocomplete = new google.maps.places.Autocomplete(gmapSearchInput);

google.maps.event.addListener(gmapAutocomplete, 'place_changed', function() {
    var locationPlace = gmapAutocomplete.getPlace();
    window.location = `/map/${locationPlace.geometry.location.lng()},${locationPlace.geometry.location.lat()}/`;
});