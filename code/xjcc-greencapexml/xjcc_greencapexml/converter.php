<?php
$path = getenv('COMPOSER_HOME');
if ($path === FALSE || empty($path)) {
    $path = __DIR__;
}
require_once($path . "/vendor/autoload.php");

$input = stream_get_contents(STDIN);
if (in_array("-d", $argv) || in_array("--decode", $argv)) {
    $data = json_decode($input, true);
    $output = new \GreenCape\Xml\Converter($data);
} else {
    $xml = new \GreenCape\Xml\Converter($input);
    $output = json_encode($xml->data);
}
echo $output;
?>
