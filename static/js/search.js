document.addEventListener('DOMContentLoaded', function () {
    mapboxgl.accessToken = 'pk.eyJ1IjoicGFya3dlbGwiLCJhIjoiY2tybHBmNm81MG9mejJubDdsYWtrbTAwcyJ9.qMieRcLq9CxLIaPeoBZi1Q';
    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        placeholder: 'Where are you going?',
        mapboxgl: mapboxgl,
    });
    geocoder.addTo('#geocoderSearchBarHome');
    
    geocoder.on('result', e => {
        var searchResult = e.result.place_name;
        window.location = `/map/${searchResult}/`;
    })
}, false);