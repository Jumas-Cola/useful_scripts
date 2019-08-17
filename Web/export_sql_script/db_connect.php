<?php

$driver = 'mysql';
$host = 'localhost';
$db_name = 'id2545188_ban_center';
$db_user = 'id2545188_user';
$db_pass = 'AR9b7!_xu@7Y';
$charset = 'utf8';
$options = [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION];
try {
    $pdo = new
    PDO("$driver:host=$host;dbname=$db_name;charset=$charset", $db_user, $db_pass, $options);
} catch (PDOException $e) {
    die("Can't connect to database.");
}

date_default_timezone_set('Europe/Moscow');
