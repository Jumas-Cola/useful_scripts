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

$success_url = '../test.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = check_input($_POST['username']);

    if (!preg_match("/^[a-zA-Z0-9_]*$/", $username)) {
        $_SESSION['msg'] = "Username should not contain space and special characters!";
        header('location: ../auth.php');
    } else {

        $fusername = $username;
        $password = check_input($_POST["password"]);
        $fpassword = md5($password);

        $stmt = $pdo->prepare("SELECT * FROM user WHERE username=:fusername and password=:fpassword");
        $stmt->bindParam(":fusername", $fusername);
        $stmt->bindParam(":fpassword", $fpassword);
        try {
            $stmt->execute();
        } catch (PDOException $e) {
            $_SESSION['msg'] = "Can't connect to database.";
            header('location: ../auth.php');
        }

        $row = $stmt->fetchAll();
        if (empty($row)) {
            $_SESSION['msg'] = "Login Failed, Invalid Input!";
            header('location: ../auth.php');
        } else {

            if ($row[0]['access'] == 1) {
                $value = md5($row[0]['username'] . $row[0]['password']);
                setcookie("au", $value, time() + 48 * 3600, "/");
                setcookie("id", $row[0]['userid'], time() + 48 * 3600, "/");
                ?>
                <script>
                    window.location.href = <?php echo "\"" . $success_url . "\""; ?>;
                </script>
                <?php
            }
        }

    }
}
?>