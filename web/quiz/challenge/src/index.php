<?php
session_start();
require_once "config.php";

if (!isset($_SESSION['username'])) {
    header('Location: /login.php');
    exit();
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Easy Quiz</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="content">
            <h2>Easy Quiz</h2>
            <p>Welcome <?php echo htmlspecialchars($_SESSION['username']) ?>!</p>
            <p>Choose a topic to start the quiz:</p>
            <ul>
                <li><a href="quiz.php?topic=George Washington">George Washington</a></li>
                <li><a href="quiz.php?topic=Isaac Newton">Isaac Newton</a></li>
                <li><a href="quiz.php?topic=CTF">CTF</a></li>
                <li><a href="quiz.php?topic=Random">Random</a></li>
            </ul>
            <p><a href="logout.php">Logout</a></p>
        </div>
    </body>
</html>