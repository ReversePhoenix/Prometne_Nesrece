<?php
session_start();
/**
 * Created by PhpStorm.
 * User: Rok
 * Date: 6. 01. 2017
 * Time: 21:43
 */

include('phpgraphlib.php');

$hostname="localhost";
$username="root";
$password="";
$databaseName="db";

$connect = mysqli_connect($hostname, $username, $password, $databaseName);
$query = "SELECT id_nesrece, COUNT(klas_nesrece) as kount, klas_nesrece FROM `nesreca` GROUP by klas_nesrece";

$res = mysqli_query($connect, $query);
$data1y = array();
while($row = mysqli_fetch_array($res)) {
        echo "$row[0], $row[2], $row[1]<br/>";
        array_push($data1y, $row[1]);

}

$graph = new PHPGraphLib(500,350);
$data = array(12124, 5535, 43373, 22223, 90432, 23332, 15544, 24523,
    32778, 38878, 28787, 33243, 34832, 32302);
$graph->addData($data);
$graph->setTitle('Widgets Produced');
$graph->setGradient('red', 'maroon');
$graph->createGraph();
?>
