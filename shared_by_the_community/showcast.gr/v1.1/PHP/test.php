<a href="<?php echo $_SERVER['DOCUMENT_ROOT']."/Output/MSG/ARMRGB_FDK/"; ?>">go with php</a>
<a href="<?php echo "/Output/MSG/ARMRGB_FDK/"; ?>">go with php2</a>
    <br />
<a> <?php echo $_SERVER['DOCUMENT_ROOT']."/Output/MSG/ARMRGB_FDK/"; ?></a>

<?php echo (function_exists('json_encode'))?'installed':'not installed'; ?>


<?php
	phpinfo();
?>