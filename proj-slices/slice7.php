<?php
$nis=$_POST['nis'];
$query1="SELECT *FROM siswa WHERE nis='";
$query2="$nis'";
$query=$query1 . $query;
$q=mysql_query($query,$koneksi);
?>