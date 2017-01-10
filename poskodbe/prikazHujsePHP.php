<?php

require("phpsqlajax_dbinfo.php");

// Start XML file, create parent node

$dom = new DOMDocument("1.0");
$node = $dom->createElement("markers");
$parnode = $dom->appendChild($node);

// Opens a connection to a MySQL server

$connection=mysql_connect ('localhost', $username, $password);
if (!$connection) {  die('Not connected : ' . mysql_error());}

// Set the active MySQL database

$db_selected = mysql_select_db($database, $connection);
if (!$db_selected) {
    die ('Can\'t use db : ' . mysql_error());
}

// Select all the rows in the markers table

$query = "SELECT nesreca.id_nesrece, nesreca.klas_nesrece, krajevne_lastnosti.tip, krajevne_lastnosti.vzrok, nesreca.x, nesreca.y FROM nesreca INNER JOIN krajevne_lastnosti ON nesreca.id_nesrece = krajevne_lastnosti.id_nesrece WHERE nesreca.x > 1 and nesreca.y > 1 and nesreca.klas_nesrece = 'H'  LIMIT 300";
$result = mysql_query($query);
if (!$result) {
    die('Invalid query: ' . mysql_error());
}

header("Content-type: text/xml");

// Iterate through the rows, adding XML nodes for each

while ($row = @mysql_fetch_assoc($result)){
    // Add to XML document node
    $node = $dom->createElement("marker");
    $newnode = $parnode->appendChild($node);
    $newnode->setAttribute("id",$row['id_nesrece']);
    $newnode->setAttribute("klas_nesrece",$row['klas_nesrece']);
    $newnode->setAttribute("vzrok",$row['vzrok']);
    $newnode->setAttribute("tip",$row['tip']);
    $newnode->setAttribute("lat",$row['x']);
    $newnode->setAttribute("lod",$row['y']);


}

echo $dom->saveXML();
//datoteka za kreiranje PHP DOM dokumenta , ki nam naredi XML, XML ustavimo v downloadURL
?>