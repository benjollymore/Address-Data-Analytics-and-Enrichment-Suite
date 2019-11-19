<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Address Enrichment Center</title>
	<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
	<script src = "https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
	<meta name="viewport" content="width=device-width, height=device-height initial-scale=1.0 shrink-to-fit=no">


    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css" integrity="sha384-Smlep5jCw/wG7hdkwQ/Z5nLIefveQRIY9nfy6xoR1uRYBtpZgI6339F5dgvm/e9B" crossorigin="anonymous">
    <link rel = "stylesheet" href = "https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
    <style>
      td {padding-left:  1%;}
    </style>
    <script>var FileID; </script>
</head>

<body>
	<script> 
		
		var loaded = false;

		$(document).on("pageshow", function () {
			if ($('.ui-page-active').attr('id') ==
			    "page1") {
				initialize('addresses.txt')
			  } 
			else if ($('.ui-page-active').attr('id') ==
			    "Page2") {
			  		loadData();

			  } 
			});

	</script>

	<div data-role="page" id="page1">
	
	<div class="container">
	 <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	  <a class="navbar-brand" href="#"><img src="service-canada-logo.jpg" width="100" height="50" alt="" ></a>
	  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
	    <span class="navbar-toggler-icon"></span>
	  </button>
	  <div class="collapse navbar-collapse" id="navbarText">
	    <ul class="navbar-nav mr-auto">
	      <li class="nav-item active">
	        <a class="nav-link" href="#Page2">Address Lookup<span class="sr-only">(current)</span></a>
	      </li>
	      <li class="nav-item">
	        <a class="nav-link" href="#page1">Address Database</a>
	      </li>
	      <li class="nav-item">
	        <a class="nav-link" href="#">Other Resources</a>
	      </li>
	    </ul>
	  </div>
	</nav>



		<script>
			
			function getJSONData(number)
			{
				FileID ="/JSON_FILES/" + number + ".json";
				console.log(FileID);
				//$.mobile.changePage("Page2");

			}

			function getJSONData2(number)
			{

				file ="/JSON_FILES/" + number + ".json";
				jquery.getJSON(file, function(json){

			//build address
			document.getElementById('addr').innerHTML = "<b>Address:</b><br>";
			document.getElementById('addr').innerHTML += json.address.number + " ";
			document.getElementById('addr').innerHTML += json.address.street + "<br>";
			document.getElementById('addr').innerHTML += json.address.neighborhood + "<br>";
			document.getElementById('addr').innerHTML += json.address.city + "<br>";
			document.getElementById('addr').innerHTML += json.address.muncipality + "<br>";
			document.getElementById('addr').innerHTML += json.address.province + "<br>";
			document.getElementById('addr').innerHTML += json.address.country + "<br>";
			document.getElementById('addr').innerHTML += json.address.postal_code + "<br>";

  			//build mailing info
  			document.getElementById('mail').innerHTML = "<br><b>Mailing Information:</b><br>";
  			document.getElementById('mail').innerHTML += json.address.number + " ";
  			document.getElementById('mail').innerHTML += json.address.street + "<br>";
  			document.getElementById('mail').innerHTML += json.address.neighborhood + "<br>";
  			document.getElementById('mail').innerHTML += json.address.city + "<br>";
  			
  			//build business info
  			if (json.businesses){
  				document.getElementById('bus').innerHTML = "<br><b>Businesses at this Address:</b><br>";
  				for (i =0 ; i < json.businesses.length; i++){
  					document.getElementById('bus').innerHTML += json.businesses[i].name + "<br>";
  					document.getElementById('bus').innerHTML += json.businesses[i].vicinity + "<br>";
  					//for (j = 0; i <  json.businesses[i].types.length; j++){
  					document.getElementById('bus').innerHTML += json.businesses[i].types + "<br><br>";
  					//}
  				}
  			}
  			else{
  				document.getElementById('bus').innerHTML = "";
  			}

  			//street view info
  			document.getElementById('street').innerHTML = "<br><b>Street Level View:</b><br>";
  			document.getElementById('street').innerHTML += "Building Type Prediction from Neural Network: " + json.streetClass + "<br>";
  			document.getElementById('street').innerHTML += "<iframe width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0\"src=\"https://www.google.com/maps/embed/v1/streetview?location=" + json.lattitude + "," + json.longitude + "&pitch=10&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8\" allowfullscreen></iframe><br>";
  			
  			//sattelite info
  			document.getElementById('satellite').innerHTML = "<br><b>Satellite View:</b><br>";
  			document.getElementById('satellite').innerHTML += "Terrain Type Prediction from Neural Network: " + json.satClass + "<br>";
  			document.getElementById('satellite').innerHTML += "<iframe width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0\"src=\"https://www.google.com/maps/embed/v1/view?center=" + json.lattitude + "," + json.longitude + "&zoom=18&maptype=satellite&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8\" allowfullscreen></iframe><br>";
  		});

			}

			function initialize(file){
				if(!loaded){
				var addresses;
				var rawFile = new XMLHttpRequest();
				rawFile.open("GET", file, false);
				rawFile.onreadystatechange = function ()
				{
					if(rawFile.readyState === 4)
					{
						if(rawFile.status === 200 || rawFile.status == 0)
						{
							var allText = rawFile.responseText;
							console.log(allText);
							addresses = allText.split('\n');
							console.log(addresses);
						}
					}
				}
				rawFile.send(null);

				for (i = 0; i < addresses.length; i++){
					document.getElementById('nav').innerHTML += 
					"<button onclick=\"getJSONData(" + i + ")\" style=\"width: 98%; margin-left: 1%; margin-right: 10%; margin-top: 15px;\"><a href=#Page2>" + addresses[i] + "</a></button><br>";
				}

				loaded = true;}
			}

		</script>
		<div id="nav"></div>
		<hr>
		<div id="info">
			<div id="addr"></div>
			<div id="mail"></div>
			<div id="bus"></div>
			<div id="street"></div>
			<div id="satellite"></div>
			<div id="people"></div>
			<div id="flags"></div>
		</div>

	</div>
</div>
	<div data-role="page" id="Page2">
		<script>
			function loadData() {
				console.log(FileID);
			jQuery.getJSON(FileID, function(json)
			{

				//build address
				//document.getElementById('street').innerHTML = "<b>Address:</b><br>";
				document.getElementById('StreeNum').innerHTML = json.address.number;
				console.log(json.address.number);
				document.getElementById('StreetName').innerHTML = json.address.street;
				document.getElementById('Neighborhood').innerHTML = json.address.neighborhood;
				document.getElementById('City').innerHTML = json.address.city;
				document.getElementById('Muncipality').innerHTML = json.address.muncipality;
				document.getElementById('Province').innerHTML = json.address.province;
				document.getElementById('Country').innerHTML = json.address.country;
				document.getElementById('PostalCode').innerHTML = json.address.postal_code;

				document.getElementById('StreetView').innerHTML = "<iframe width=\"100%\" height=\"300\" frameborder=\"0\" style=\"border:0\"src=\"https://www.google.com/maps/embed/v1/streetview?location=" + json.lattitude + "," + json.longitude + "&pitch=10&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8\" allowfullscreen></iframe>";
				document.getElementById('SatView').innerHTML = "<iframe width=\"100%\" height=\"300\" frameborder=\"0\" style=\"border:0\"src=\"https://www.google.com/maps/embed/v1/view?center=" + json.lattitude + "," + json.longitude + "&zoom=18&maptype=satellite&key=AIzaSyCgcV2R4KkxhqdnzXXMAbYA4VLEBQd7w-8\" allowfullscreen></iframe>";
			});
		}
		</script>

	    <div class="container">
	      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	      <a class="navbar-brand" href="#"><img src="service-canada-logo.jpg" width="100" height="50" alt="" ></a>
	      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
	        <span class="navbar-toggler-icon"></span>
	      </button>
	      <div class="collapse navbar-collapse" id="navbarText">
	        <ul class="navbar-nav mr-auto">
	          <li class="nav-item active">
	            <a class="nav-link" href="#">Address Lookup<span class="sr-only">(current)</span></a>
	          </li>
	          <li class="nav-item">
	            <a class="nav-link" href="#page1">Address Database</a>
	          </li>
	          <li class="nav-item">
	            <a class="nav-link" href="#">Other Resources</a>
	          </li>
	        </ul>
	      </div>
	    </nav>
	    <div class="row">
	      <!-- -->
	      <div class="col-8">
	        <div class ="jumbotron" style="margin-left:15px;margin-right: 0px; margin-bottom: 15px;margin-top: 15px; padding: 15px">
	          <h2> 
	            <input type="text" style="min-width: 70%; height: 40px; margin-left: 1%; margin-right: 1%">
	            <button class="btn btn-primary" type="button" style="width: 26%; margin-right=:1%; height: 40px; margin-top: -10px">Address Search</button>
	          </h2>
	        </div>

	        <div class ="jumbotron" style="margin-left:15px;margin-right: 0px; margin-bottom: 15px;margin-top: 15px; padding: 15px">
	          <div class="card-deck">
	            <div class="card">
	              <h5 class="card-header bg-danger">Post Office</h5>
	              <div class="card-body">
	                <p class="card-text">This location is flagged as a post office. Verify address is not a PO box.</p>
	              </div>
	              <div class="card-footer">
	                <small class="text-muted">Post Office Flag Triggered</small>
	              </div>
	            </div>
	            <div class="card">
	              <h5 class="card-header bg-warning">Mixed Location</h5>
	              <div class="card-body">
	                <p class="card-text">This location may be mixed residential and commerical.</p>
	              </div>
	              <div class="card-footer">
	                <small class="text-muted">Address has businesses</small>
	              </div>
	            </div>
	            <div class="card">
	                <h5 class="card-header bg-info">Bus Route</h5>
	              <div class="card-body">
	                <p class="card-text">This location is a bus root.</p>
	              </div>
	              <div class="card-footer">
	                <small class="text-muted">Bus Route Flag</small>
	              </div>
	            </div>
	          </div>
	        </div>

	        <div class ="jumbotron bg-light" style="margin-left:15px;margin-right: 0px; margin-bottom: 15px;margin-top: 15px; padding: 15px">
	         
	          <nav>
	            <div class="nav nav-tabs" id="nav-tab" role="tablist">
	              <a class="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab" aria-controls="nav-home" aria-selected="true">Address Data</a>
	              <a class="nav-item nav-link" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab" aria-controls="nav-profile" aria-selected="false">Business Data</a>
	              <a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-contact" role="tab" aria-controls="nav-contact" aria-selected="false">Other Info</a>
	            </div>
	          </nav>
	          <div class="tab-content" id="nav-tabContent">
	            <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
	              <br>
	              <table class="table-bordered table-hover table-striped" style="margin-right: 1%; width: 98%; margin-left:  1%; "> 
	                <thead class="table-dark">
	                  <tr>
	                    <th style="text-align: center">Field</th>
	                    <th style="text-align:  center">Value</th>
	                  </tr>
	                </thead>
	                <tbody> 
	                <tr><td>Number</td><td id="StreeNum">5595</td></tr>
	                <tr><td>Street</td><td id="StreetName">Fenwick Street</td></tr>
	                <tr><td>Neighborhood</td><td id="Neighborhood">South End</td></tr>
	                <tr><td>Locality</td><td id="Locality">Halifax</td></tr>
	                <tr><td>City</td><td id ="City">Halifax</td></tr>
	                <tr><td>Muncipality</td><td id="Muncipality">Halifax Regional Municipality</td></tr>
	                <tr><td>Province</td><td id="Province">Nova Scotia</td></tr>
	                <tr><td>Country</td><td id="Country">Canada</td></tr>
	                <tr><td>Postal Code</td><td id="PostalCode">B3H 4M2</td></tr>


	                </tbody>
	              </table>


	            </div>
	            <div class="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">

	            ..sfsdf.
	          </div>
	            <div class="tab-pane fade" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">Other Information Can Go here</div>
	          </div>
	          </div>
	      </div>

	      <!-- MAPS STUFF -->
	      <div class="col-4" style="margin-right: 15px; margin-left: -15px">
	        <div class="card" style="margin-top: 15px">
	                <h5 class="card-header bg-secondary">Street View</h5>
	              <div class="card-body bg-secondary" id="StreetView">
	                <iframe src="https://www.google.com/maps/embed?pb=!4v1574136651625!6m8!1m7!1sn4kdeobKqhaBsaBKydVeqw!2m2!1d44.63049246863288!2d-63.58225347839939!3f143.13222998123817!4f0!5f0.7820865974627469" width=100% height="300" frameborder="0" style="border:0;" allowfullscreen=""></iframe>
	              </div>
	              <div class="card-footer">
	                <small class="text-muted">Address map</small>
	              </div>
	            </div>

	            <div class="card" style="margin-top: 15px">
	                <h5 class="card-header bg-secondary">Satellite Image</h5>
	              <div class="card-body bg-secondary" id="SatView">
	                <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d2494.2991792068888!2d-63.58283926117638!3d44.63107297040737!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2sca!4v1574137000127!5m2!1sen!2sca" width=100% height="300" frameborder="0" style="border:0;" allowfullscreen=""></iframe>  
	              </div>
	              <div class="card-footer">
	                <small class="text-muted">Address map</small>
	              </div>
	            </div>
	              

	        </div>

      </div>
    </div>

		</div>
<!--
		<form action="/echo" method="POST">
			<input name="text" placeholder="Enter an address to query here!" required>
			<br>
			<input type="submit" onclick="aWellNamedFunctionThatDoesStuff()" value="Query Address">
			
		</form>

		<div id="wait"></div>
	</div>

	<script>
		function aWellNamedFunctionThatDoesStuff(){
			document.getElementById("wait").innerHTML = "<h2>Parsing your query...</h2>";
		}

	</script>
	--->
	

	<br><br>

    <!-- <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script> -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/js/bootstrap.min.js" integrity="sha384-o+RDsa0aLu++PJvFqy8fFScvbHFLtbvScb8AjopnFD+iEQ7wo/CG0xlczd+2O/em" crossorigin="anonymous"></script>
</body>
</html>