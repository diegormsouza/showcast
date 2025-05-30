<?php

error_reporting(0);
ini_set('display_errors', 1);
error_reporting(E_ALL);

$requestData = json_decode(file_get_contents('php://input'), true);
//$requestData = file_get_contents('php://input');
$folderUrl = $requestData["folderUrl"];
$fileTypes = $requestData["fileTypes"];
$isLocal = $requestData["isLocal"];

if (substr($folderUrl, -1) != '/') {
    $folderUrl .= '/';
}

$files = [];
$result = [];
if ($isLocal) {
    $files = scandir("{$_SERVER['DOCUMENT_ROOT']}" . $folderUrl);
    if($files===false) echo false;
}

$filterTypes = function ($mimeTypes) use ($files, $folderUrl) {
    $result = array();
    $i = 0;
    foreach ($files as $file) {
        $mimeType = mime_content_type("{$_SERVER['DOCUMENT_ROOT']}" . $folderUrl . $file);
        foreach ($mimeTypes as $type) {
            if (strcmp($mimeType, $type)==0) {
                $result[$i++] = "http://{$_SERVER['SERVER_NAME']}" . $folderUrl . $file;
            }
        }
    }
    return $result;
};
    
switch ($fileTypes) { //WARNING: not using 'all' requires file-checking one by one, and causes significant delay for large directories
    case 'all':
        $i=0;
        foreach ($files as $file) {
            $result[$i++] = "http://{$_SERVER['SERVER_NAME']}" . $folderUrl . $file;
        }
        break;

    case 'image':
        if ($isLocal == false) {
            // Get cURL resource
            $curl = curl_init();
            // Set some options - we are passing in a useragent too here
            curl_setopt_array($curl, [
                CURLOPT_RETURNTRANSFER => 1,
                CURLOPT_URL => $folderUrl
            ]);
            // Send the request & save response to $resp
            $resp = curl_exec($curl);
            // Close request to clear up some resources
            curl_close($curl);
        
            //filter response to get urls
            preg_match_all('/(?<=href=").*?(?=">W)/', $resp, $matches);
            foreach ($matches[0] as &$match) {
                $match=$folderUrl.$match;
            }
//            echo json_encode($matches[0]);
            $result = $matches[0];
        } else {
            $mimeTypes=["image/gif","image/jpg","image/jpeg","image/png"];
            $result = $filterTypes($mimeTypes);
        }
        break;

    case 'text':
        $mimeTypes=["text/plain"];
        $result = $filterTypes($mimeTypes);
        break;
    case 'binary':
        $mimeTypes=["application/octet-stream"];
        $result = $filterTypes($mimeTypes);
        break;
}

echo json_encode($result);
//echo $result."......."."$requestData";
?>