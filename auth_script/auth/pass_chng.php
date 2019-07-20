<?php
include('db_connect.php');
session_start();
function check_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = check_input($_POST['username']);
    $old_pass = md5(check_input($_POST["old_pass"]));
    $new_pass = md5(check_input($_POST["new_pass"]));

    $stmt = $pdo->prepare("SELECT * FROM user WHERE username=:username AND password=:old_pass");
    $stmt->bindParam(":username", $username);
    $stmt->bindParam(":old_pass", $old_pass);

    try {
        $stmt->execute();
    } catch (PDOException $e) {
        $_SESSION['msg'] = "Can't connect to database.";
        header('location: change_pass.php');
    }

    $row = $stmt->fetchAll();
    if (empty($row)) {
        $_SESSION['msg'] = "Failed, Invalid Input!";
        header('location: change_pass.php');
    } else {
        $stmt = $pdo->prepare("UPDATE user SET password=:new_pass WHERE username=:username and password=:old_pass");
        $stmt->bindParam(":username", $username);
        $stmt->bindParam(":old_pass", $old_pass);
        $stmt->bindParam(":new_pass", $new_pass);
        try {
            $stmt->execute();
        } catch (PDOException $e) {
            $_SESSION['msg'] = "Can't connect to database.";
            header('location: change_pass.php');
        }
        $_SESSION['msg'] = "Password changed!";
        header('location: change_pass.php');
    }
}