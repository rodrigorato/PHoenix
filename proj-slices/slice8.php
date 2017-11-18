<?php
$nis=$_POST['nis'];
if ($indarg == "") {$query="SELECT *FROM siswa WHERE nis='$nis'";}
else {$query="SELECT *FROM siswa WHERE nis='$indarg'";}
$q=mysql_query($query,$koneksi);
?>