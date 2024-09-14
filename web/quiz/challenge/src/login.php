<?php
session_start();
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if (!empty($username) && !empty($password)) {
        $stmt = $pdo->prepare('SELECT password FROM users WHERE username = ?');
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['username'] = $username;
            header('Location: /');
            exit();
        } else {
            echo "Invalid username or password.";
        }
    } else {
        echo "Please fill in all fields.";
    }
}
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="content">
            <form method="POST" action="login.php">
                Username: <input type="text" name="username" required>
                Password: <input type="password" name="password" required>
                <button type="submit">Login</button>
            </form>
        </div>
        <br>
        <div class="content">
            Don't have an account yet? Click here to <a href="register.php">register</a>
        </div>
    </body>
</html>