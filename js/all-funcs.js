var opts = {
          lines: 13, // The number of lines to draw
          length: 30, // The length of each line
          width: 10, // The line thickness
          radius: 30, // The radius of the inner circle
          corners: 1, // Corner roundness (0..1)
          rotate: 0, // The rotation offset
          direction: 1, // 1: clockwise, -1: counterclockwise
          color: '#000', // #rgb or #rrggbb or array of colors
          speed: 1, // Rounds per second
          trail: 60, // Afterglow percentage
          shadow: false, // Whether to render a shadow
          hwaccel: false, // Whether to use hardware acceleration
          className: 'spinner', // The CSS class to assign to the spinner
          zIndex: 2e9, // The z-index (defaults to 2000000000)
          top: '50%', // Top position relative to parent
          left: '50%' // Left position relative to parent
        };

        
        var res_container = document.getElementById("restaurant-container");
        var res_name = document.getElementById("restaurant_name");
        var res_kind = document.getElementById("restaurant_kind");
        var res_address = document.getElementById("restaurant_address");
        var spinner = document.getElementById('loading-indicator');
        var spin = new Spinner();
            
        var current_restaurant = {}    
        var restaurants_list = {}
        
        var location_btn = document.getElementById("location_btn");
        location_btn.addEventListener('click', getLocation);
        
        var yes_btn = document.getElementById("yes_btn");
        yes_btn.addEventListener('click', show_restaurant_address);
        
        var no_btn = document.getElementById("no_btn");
        no_btn.addEventListener('click', choose_random_restaurant);
        
        function getLocation() {
            // Hide 
            hideAll();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(sendLocation, handle_error);
            } else {
                res_name.innerHTML = "Geolocation is not supported by this browser.";
            }
        }
        
        function sendLocation(position) {     
            var location = {}
            location['latitude'] = position.coords.latitude
            location['longitude'] = position.coords.longitude
                
            $.ajax({
               url: '/',
                type: 'POST',
                data: JSON.stringify(location),
                contentType: 'application/json',
                success: on_request_success,
                error: on_request_error  
            });	
        }
        
        $(document).ajaxSend(function(event, request, settings) {
            //$('#loading-indicator').show();
            spin.spin();
            spinner.appendChild(spin.el);
        });

        $(document).ajaxComplete(function(event, request, settings) {
            //$('#loading-indicator').hide();
            spin.stop();
        });
        
        function handle_error(err) {
            if (err.code == 1) {
                console.debug('PERMISSION_DENIED');
                res_name.innerHTML = "Permission denied";
            } else if (err.code == 2) {
                console.debug('POSITION UNAVAILABLE');
                res_name.innerHTML = "Position unavailable";
            } else if (err.code == 3) {
                console.debug('TIMEOUT');
                res_name.innerHTML = "timeout";
            } else {
                console.debug('SOMETHING ELSE WENT WRONG GETTING GEOLOCATION');
                res_name.innerHTML = "Something went wrong";
            }
        }
        
        function choose_random_restaurant() { 
            hide_restaurant_address();
            var index_chosen = choose_random_restaurant_index();    
            
            if (index_chosen != -1) {
                current_restaurant = restaurants_list[index_chosen]
                show_restaurant();
                restaurants_list.splice(index_chosen, 1);
            } else {
                current_restaurant = {}
                res_name.innerHTML = "Sorry, no restaurants left :("
                res_kind.innerHTML = "";
                document.getElementById("no_btn").style.display = "none";
                document.getElementById("yes_btn").style.display = "none";
            }
        }
        
        function show_restaurant() {
            var all_categories = [];
            for (var i = 0; i < current_restaurant.categories.length; i++) { 
                all_categories.push(current_restaurant.categories[i][0]);
            }  
            
            res_name.innerHTML = current_restaurant.name
            res_kind.innerHTML = all_categories.join(", ");
        }
        
        function choose_random_restaurant_index() {
            if (restaurants_list.length != 0) {
                return Math.floor((Math.random() * restaurants_list.length));                   
            } else {
                return -1;
            }
        }
        
        function show_restaurant_address() {
            res_address.innerHTML = current_restaurant.location.display_address;
        }
        
        function hide_restaurant_address() {
            res_address.innerHTML = "";
        }
        
        function showAll() {
            res_container.style.display = 'block';
        }
        
        function hideAll() {
            res_container.style.display = 'none';
        }
        
        function on_request_success(response) {
            showAll();
            document.getElementById("no_btn").style.display = "inline";
            document.getElementById("yes_btn").style.display = "inline";
            
            obj = JSON.parse(response);
            restaurants_list = obj.businesses
            console.debug('restaurants', restaurants_list)
            choose_random_restaurant()
        } 
            
        function on_request_error(r, text_status, error_thrown) {
            console.debug('error', text_status + ", " + error_thrown + ":\n" + r.responseText);
        }