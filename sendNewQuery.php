<?php 

$query = $_POST['query'];
$query = '"'.$query.'"';
$operator = "python appendToAddresses.py ".$query;
$index = shell_exec($operator);

$jsonGenerator = 

echo $output;

?>