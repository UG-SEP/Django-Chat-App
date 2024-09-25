$(document).on("click",'.location-btn',function(event){
    $(document).on("click",'.location-btn',function(event){
        getLocation()
        .then((location) => {
            if (!location || isNaN(location.latitude) || isNaN(location.longitude)) {
              console.error("Invalid location:", location);
              return;
            }
            console.log(location.latitude, location.longitude);
            initMap(location.latitude, location.longitude);
        })
        .catch((error) => {
            console.log(error);
        });
    });
    });
    function initMap(latitude,longitude) {
        
        var mapProp= {
            center:new google.maps.LatLng(latitude,longitude),
            zoom:5,
        };
        var map = new google.maps.Map(document.getElementById('map'), mapProp);
    }
    function getLocation(){
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        var latitude = position.coords.latitude;
                        var longitude = position.coords.longitude;
                        console.log(latitude, longitude);
                        resolve({'latitude':latitude,'longitude':longitude});
                    },
                    function(error) {
                        switch (error.code) {
                            case error.PERMISSION_DENIED:
                                alert("User denied the request for Location.");
                                reject();
                                break;
                            case error.POSITION_UNAVAILABLE:
                                alert("Location information is unavailable.");
                                reject();
                                break;
                            case error.TIMEOUT:
                                alert("The request to get user location timed out.");
                                reject();
                                break;
                            case error.UNKNOWN_ERROR:
                                alert("An unknown error occurred.");
                                reject();
                                break;
                        }
                    }
                );
            } else {
                console.log("Location is not supported by this browser.");
                reject();
            }
        });
    }