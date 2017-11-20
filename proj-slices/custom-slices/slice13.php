<?php
$cars = array("Yes", "No");
$cars[1] = $_POST['nis'];
$q=mysql_query($cars[1],$koneksi);
?>
