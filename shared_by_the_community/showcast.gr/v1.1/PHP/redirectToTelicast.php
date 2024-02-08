<?php
//redirect to telicast client http

//get server IP
//echo $_SERVER['SERVER_ADDR'];
$self_IP = $_SERVER['SERVER_ADDR'];

//redirection to telicast
header("Location: http://".$self_IP.":8100");
exit();


?>