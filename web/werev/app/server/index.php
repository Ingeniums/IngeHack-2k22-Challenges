<?php
if(isset($_GET['file']) && $_GET['file'] != '' && is_string($_GET['file'])) {
    $x = file_get_contents($_GET['file']);
    echo $x;
    die();
}
phpinfo();
;
