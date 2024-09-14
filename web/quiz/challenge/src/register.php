<?php
session_start();
require_once 'config.php';

$stmt = $pdo->query("SELECT name FROM sqlite_master WHERE type='table' AND name='users'");
if ($stmt->fetchColumn() === false) {
    $stmt = $pdo->prepare('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)');
    $stmt->execute();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    if (!empty($username) && !empty($password)) {
        try {
            $stmt = $pdo->prepare('INSERT INTO users (username, password) VALUES (?, ?)');
            $stmt->execute([$username, $hashed_password]);
            header('Location: login.php');
            exit();
        } catch (PDOException $e) {
            if ($e->getCode() == 23000) {
                echo "Username already taken.";
            } else {
                echo "Error: Could not register user.";
            }
        }
    } else {
        echo "Please fill in all fields.";
    }
}
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Register</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="content">
            <form method="POST" action="register.php">
                Username: <input type="text" name="username" required>
                Password: <input type="password" name="password" required>
                <button type="submit">Register</button>
            </form>
        </div>
        <br>
        <div>
            Already have an account? Click here to <a href="login.php">log in</a>
        </div>
    </body>
</html>
