var x = document.getElementById("map");
var gmapGeocoder = new google.maps.Geocoder();
var gmapSearchInputMap = document.querySelector("#gmapSearchInputMap");
gmapAutocompleteMap = new google.maps.places.Autocomplete(gmapSearchInputMap);


company_listing = []
park_listing = []
for (let companyItem = 0; companyItem < company.length; companyItem++) {
    const element = {
        "id": company[companyItem].id,
        "logo": company[companyItem].company_logo,
        "name": company[companyItem].company_name,
        "admin": company[companyItem].administrator,
        "email": company[companyItem].company_email,
    };
    company_listing.push(element)
}
for (let partItem = 0; partItem < parks.length; partItem++) {
    const element = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [parseFloat(parks[partItem].park_lon), parseFloat(parks[partItem].park_lat)],
            "lon": [parseFloat(parks[partItem].park_lon)],
            "lat": [parseFloat(parks[partItem].park_lat)],
        },
        "properties": {
            "id": parks[partItem].id,
            "phone": parks[partItem].park_number,
            "email": parks[partItem].park_email,
            "address": parks[partItem].park_address.slice(0, 30).concat('...'),
            "name": parks[partItem].park_name.slice(0, 30).concat('...'),
            "closing_time": parks[partItem].park_closing_time,
            "info": parks[partItem].park_about.slice(0, 100).concat('...'),
            "company": parks[partItem].company_id,
        }
    };
    park_listing.push(element)
}

document.addEventListener('DOMContentLoaded', function () {
    if (navigator.geolocation) {
        mapboxgl.accessToken = 'pk.eyJ1IjoicGFya3dlbGwiLCJhIjoiY2tybHBmNm81MG9mejJubDdsYWtrbTAwcyJ9.qMieRcLq9CxLIaPeoBZi1Q';
        navigator.geolocation.getCurrentPosition(position => {
            var map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [position.coords.longitude, position.coords.latitude],
                zoom: 15,
            });
            map.addControl(new mapboxgl.NavigationControl());
            var from_location = [position.coords.longitude, position.coords.latitude]

            google.maps.event.addListener(gmapAutocompleteMap, 'place_changed', function () {
                var locationPlaceMap = gmapAutocompleteMap.getPlace();
                map.flyTo({
                    center: [locationPlaceMap.geometry.location.lng(), locationPlaceMap.geometry.location.lat()],
                    essential: true,
                    zoom: 15
                });
            });

            if (lon, lat) {
                map.flyTo({
                    center: [lon, lat],
                    essential: true,
                    zoom: 15
                });
            }

            map.on('load', function (e) {
                map.addSource('places', {
                    'type': 'geojson',
                    'data': {
                        "type": "FeatureCollection",
                        "features": park_listing
                    },
                });
                buildLocationList(park_listing);
                addMarkers()
                parkCoordinates = (coord_lon, coord_lat) => {
                    window.open(`https://maps.google.com/?daddr=${coord_lat},${coord_lon}`, '_blank');
                };

                map.addLayer({
                    "id": "circle500",
                    "type": "circle",
                    "source": "places",
                    "paint": {
                        "circle-radius": {
                            stops: [
                                [0, 0],
                                [14, 1000]
                            ],
                            base: 2
                        },
                        "circle-color": "#009a00",
                        "circle-opacity": 0.2,
                    }
                });
            });

            map.on('click', function (e) {
                var features = map.queryRenderedFeatures(e.point, {
                    layers: ['locations']
                });

                if (features.length) {
                    var clickedPoint = features[0];
                    flyToStore(clickedPoint);
                    createPopUp(clickedPoint);
                    var activeItem = document.getElementsByClassName('active');
                    if (activeItem[0]) {
                        activeItem[0].classList.remove('active');
                    }
                    var listing = document.getElementById('listing-' + clickedPoint.properties.id);
                    listing.classList.add('active');
                }
            });

            // build sidebar list
            function buildLocationList(data) {
                data.forEach((park_list, i) => {
                    var prop = park_list.properties;
                    company_listing.forEach(compInfo => {
                        if (prop.company === compInfo.id) {
                            if (Math.min(window.screen.width, window.screen.height) < 768) {
                                var listings = document.getElementById('listingSmall');
                                var listing = listings.appendChild(document.createElement('div'));

                                listing.id = "listing-" + park_list.properties.id;
                                listing.className = 'item';

                                var link = listing.appendChild(document.createElement('a'));
                                link.style.textDecoration = "none";
                                link.href = '#';
                                link.className = 'title';
                                link.id = "link-" + prop.id;
                                link.innerHTML = `${prop.name} - <small>${prop.address}</small>`;

                                var details = listing.appendChild(document.createElement('div'));
                                details.className = "detail-card"

                                var detailsParkInfo = details.appendChild(document.createElement('div'));
                                detailsParkInfo.className = "park-info"
                                detailsParkInfo.innerHTML = prop.info;

                                detailsParkInfoUL = detailsParkInfo.appendChild(document.createElement('ul'));
                                detailsParkInfoUL.className = "park-info-ul"

                                detailsParkInfoLi = detailsParkInfoUL.appendChild(document.createElement('li'));
                                detailsParkInfoLi2 = detailsParkInfoUL.appendChild(document.createElement('li'));
                                detailsParkInfoLi.className = "park-info-li"
                                detailsParkInfoLi2.className = "park-info-li"

                                detailsParkInfoLiCall = detailsParkInfoLi.appendChild(document.createElement('a'));
                                detailsParkInfoLiCall.href = `tel:${prop.phone}`;
                                detailsParkInfoLiCall.innerHTML = `mobile - ${prop.phone}`;
                                detailsParkInfoLi2.innerHTML = `closing time - ${prop.closing_time}`;

                                var detailsParkLogoDiv = details.appendChild(document.createElement('div'));
                                detailsParkLogoDiv.className = "logo-div"

                                var detailsParkA = detailsParkLogoDiv.appendChild(document.createElement('a'));
                                detailsParkA.className = "logo-a"
                                detailsParkA.style.textDecoration = "none";
                                detailsParkA.href = '#';
                                detailsParkA.id = "logo-a-" + prop.id;

                                var detailsParkLogo = detailsParkA.appendChild(document.createElement('img'));
                                detailsParkLogo.className = "logo-img"
                                detailsParkLogo.src = `/media/${compInfo.logo}`;

                                link.addEventListener('click', function (e) {
                                    for (var i = 0; i < data.length; i++) {
                                        if (this.id === "link-" + data[i].properties.id) {
                                            var clickedListing = data[i];
                                            flyToStore(clickedListing);
                                            createPopUp(clickedListing);
                                        }
                                    }
                                    var activeItem = document.getElementsByClassName('active');
                                    if (activeItem[0]) {
                                        activeItem[0].classList.remove('active');
                                    }
                                    this.parentNode.classList.add('active');
                                });

                                detailsParkA.addEventListener('click', function (e) {
                                    for (var i = 0; i < data.length; i++) {
                                        if (this.id === "logo-a-" + data[i].properties.id) {
                                            var clickedListing = data[i];
                                            flyToStore(clickedListing);
                                            createPopUp(clickedListing);
                                        }
                                    }
                                    var activeItem = document.getElementsByClassName('active');
                                    if (activeItem[0]) {
                                        activeItem[0].classList.remove('active');
                                    }
                                    this.parentNode.classList.add('active');
                                });
                            } else {
                                var listings = document.getElementById('listings');
                                var listing = listings.appendChild(document.createElement('div'));

                                listing.id = "listing-" + park_list.properties.id;
                                listing.className = 'item';

                                var link = listing.appendChild(document.createElement('a'));
                                link.style.textDecoration = "none";
                                link.href = '#';
                                link.className = 'title';
                                link.id = "link-" + prop.id;
                                link.innerHTML = `${prop.name} - <small>${prop.address}</small>`;

                                var details = listing.appendChild(document.createElement('div'));
                                details.className = "detail-card"

                                var detailsParkInfo = details.appendChild(document.createElement('div'));
                                detailsParkInfo.className = "park-info"
                                detailsParkInfo.innerHTML = prop.info;

                                detailsParkInfoUL = detailsParkInfo.appendChild(document.createElement('ul'));
                                detailsParkInfoUL.className = "park-info-ul"

                                detailsParkInfoLi = detailsParkInfoUL.appendChild(document.createElement('li'));
                                detailsParkInfoLi2 = detailsParkInfoUL.appendChild(document.createElement('li'));
                                detailsParkInfoLi.className = "park-info-li"
                                detailsParkInfoLi2.className = "park-info-li"

                                detailsParkInfoLiCall = detailsParkInfoLi.appendChild(document.createElement('a'));
                                detailsParkInfoLiCall.href = `tel:${prop.phone}`;
                                detailsParkInfoLiCall.innerHTML = `mobile - ${prop.phone}`;
                                detailsParkInfoLi2.innerHTML = `closing time - ${prop.closing_time}`;

                                var detailsParkLogoDiv = details.appendChild(document.createElement('div'));
                                detailsParkLogoDiv.className = "logo-div"

                                var detailsParkA = detailsParkLogoDiv.appendChild(document.createElement('a'));
                                detailsParkA.className = "logo-a"
                                detailsParkA.style.textDecoration = "none";
                                detailsParkA.href = '#';
                                detailsParkA.id = "logo-a-" + prop.id;

                                var detailsParkLogo = detailsParkA.appendChild(document.createElement('img'));
                                detailsParkLogo.className = "logo-img"
                                detailsParkLogo.src = `/media/${compInfo.logo}`;

                                link.addEventListener('click', function (e) {
                                    for (var i = 0; i < data.length; i++) {
                                        if (this.id === "link-" + data[i].properties.id) {
                                            var clickedListing = data[i];
                                            flyToStore(clickedListing);
                                            createPopUp(clickedListing);
                                        }
                                    }
                                    var activeItem = document.getElementsByClassName('active');
                                    if (activeItem[0]) {
                                        activeItem[0].classList.remove('active');
                                    }
                                    this.parentNode.classList.add('active');
                                });

                                detailsParkA.addEventListener('click', function (e) {
                                    for (var i = 0; i < data.length; i++) {
                                        if (this.id === "logo-a-" + data[i].properties.id) {
                                            var clickedListing = data[i];
                                            flyToStore(clickedListing);
                                            createPopUp(clickedListing);
                                        }
                                    }
                                    var activeItem = document.getElementsByClassName('active');
                                    if (activeItem[0]) {
                                        activeItem[0].classList.remove('active');
                                    }
                                    this.parentNode.classList.add('active');
                                });
                            }
                        }
                    });
                });
            };

            // interactivity
            function flyToStore(currentFeature) {
                map.flyTo({
                    center: currentFeature.geometry.coordinates,
                    zoom: 15
                });
            }

            function createPopUp(currentFeature) {
                var popUps = document.getElementsByClassName('mapboxgl-popup');
                if (popUps[0]) popUps[0].remove();

                to_location = currentFeature.geometry.coordinates;
                var distance = turf.distance(from_location, to_location, { units: 'kilometers' });

                new mapboxgl.Popup({ closeOnClick: false })
                    .setLngLat(currentFeature.geometry.coordinates)
                    .setHTML(`
                        <h5>${currentFeature.properties.name}</h5>
                        <p>
                            <i class="fa fa-lg fa-phone-alt"></i> <a href="tel:${currentFeature.properties.phone}">${currentFeature.properties.phone}</a> <br/>
                            <i class="fa fa-lg fa-map-marker-alt"></i> ${currentFeature.properties.address} <br/>
                            <i class="fa fa-lg fa-clock"></i> closing time - ${currentFeature.properties.closing_time} <br/>
                            <i class="fa fa-lg fa-envelope"></i> <a href="mailto:${currentFeature.properties.email}">${currentFeature.properties.email}</a> <br/>
                            <i class="fa fa-lg fa-route"></i> ${distance.toFixed(2)} K/m <br/>
                            <div style="background-color: #000;">
                                <!-- <a href="/booking/create/${currentFeature.properties.id}/" class="book-btn">book</a> <br/> -->
                                <button class="navigate-btn" onclick='parkCoordinates(${currentFeature.geometry.lon}, ${currentFeature.geometry.lat})'>Get direction</button> <br/>
                            </div>
                        </p>`)
                    .addTo(map);
            }

            // marker
            new mapboxgl.Marker({ color: 'red', offset: [0, -23] }).setLngLat([position.coords.longitude, position.coords.latitude]).addTo(map);
            function addMarkers() {
                park_listing.forEach(function (marker) {
                    var el = document.createElement('div');
                    el.id = "marker-" + marker.properties.id;
                    el.className = 'marker';
                    new mapboxgl.Marker(el, { offset: [0, -23] })
                        .setLngLat(marker.geometry.coordinates)
                        .addTo(map);

                    el.addEventListener('click', function (e) {
                        flyToStore(marker);
                        createPopUp(marker);
                        var activeItem = document.getElementsByClassName('active');
                        e.stopPropagation();
                        if (activeItem[0]) {
                            activeItem[0].classList.remove('active');
                        }
                        var listing = document.getElementById('listing-' + marker.properties.id);
                        listing.classList.add('active');
                    });
                });
            }
        });
    } else {
        console.log("Map couldn't load!!!");
    }
}, false);

$('#mobileParkCardTrigger, .mobile-park-card').click(function () {
    $('.mobile-park-card').toggleClass('up');
});