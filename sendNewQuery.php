<?php 
$query = $_POST['query'];
$query = '"'.$query.'"';
$operator = "python appendToAddresses.py ".$query;
$index = shell_exec($operator);
$index = substr_replace($index,"", -1);
$jsonGenerator = 'python GeoLocations.py --a --ld --pad --pld --vj --sat --wp --st '.$query.' 99 > JSON_FILES/'.$index.'.json';
$run=shell_exec($jsonGenerator);
echo "Done Processing!";
?>