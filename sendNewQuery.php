<?php 

$query = $_POST['query'];
$query = '"'.$query.'"';
$operator = "python appendToAddresses.py ".$query;
$index = shell_exec($operator);
$jsonGenerator = 'python GeoLocations.py --ld --pad --pld --vj --sat --st '.$query.' > '.$index.'.json'
shell_exec($jsonGenerator)
echo $index;

?>