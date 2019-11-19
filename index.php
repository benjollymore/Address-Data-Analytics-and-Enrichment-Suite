<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Remote command UI</title>
	<script src = "https://code.jquery.com/jquery-1.11.3.min.js"></script>
	<script src = "https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
	<meta name="viewport" content="width=device-width, height=device-height initial-scale=1">
	<link rel = "stylesheet" href = "https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
</head>

<body onload="initialize('addresses.txt')">
	<div data-role="header">
		<h1>
			Address Enrichment Suite
		</h1>
	</div>
	<div data-role="content">

		<script>


			function getJSONData(number){

				file ="/JSON_FILES/" + number + ".json";
				$.getJSON(file, function(json){

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
					document.getElementById('nav').innerHTML += "<button onclick=\"getJSONData(" + i + ")\">" + addresses[i] + "</button><br>";
				}

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


</body>
</html>