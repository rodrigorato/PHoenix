<?php
if ($a) {
    $a=$_POST["a"];
}
else {
    mysql_escape_string($a);
}
$q=mysql_query($a,$koneksi);
?>