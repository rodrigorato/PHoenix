<?php
$nis=$_POST['nis'];
while ($indarg == "") {
      $query="SELECT *FROM siswa WHERE nis='$nis'";
}
$q=mysql_query($query,$koneksi);
?>