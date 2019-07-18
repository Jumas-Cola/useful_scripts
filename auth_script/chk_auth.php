<?php
require_once('db_connect.php');

if (!isset($_COOKIE["au"]) || (trim($_COOKIE["au"]) == '')) {
    header('location: auth.php');
    exit();
}

$stmt = $pdo->prepare("SELECT * FROM user WHERE userid=:userid");
$stmt->bindParam(":userid", $_COOKIE['id']);
try {
    $stmt->execute();
} catch (PDOException $e) {
    die("Can't connect to database.");
}

$srow = $stmt->fetchAll();

if (empty($srow)) {
    $_SESSION['msg'] = "Login Failed, Invalid Input!";
    header('location: auth.php');
}

if ($_COOKIE['au'] != md5($srow[0]['access'] . $srow[0]['username'])) {
    $_SESSION['msg'] = "Login Failed, Invalid Input!";
    header('location: auth.php');
}

if ($srow[0]['access'] != 1) {
    header('location: auth.php');
    exit();
}

