<?php
$arg=$_POST['nis'];
while ($arg != "") {
    $first = substr($arg,0,1);

    if ($first=="'") { 
	$indarg = $indarg . "'"; 
    } elseif ($first==" ") {
	$indarg = $indarg . " ";
    } elseif ($first=="O") {
	$indarg = $indarg . "O";
    } elseif ($first=="R") {
	$indarg = $indarg . "R";
    } elseif ($first=="1") {
	$indarg = $indarg . "1";
    } elseif ($first=="=") {
	$indarg = $indarg . "=";
    } elseif ($first=="-") {
	$indarg = $indarg . "-";
    }
    $arg = substr($arg,1);
}
$query="SELECT *FROM siswa WHERE nis='$indarg'";
$q=mysql_query($query,$koneksi);
?>