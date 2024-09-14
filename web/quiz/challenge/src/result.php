<?php
session_start();
require_once "config.php";

if (!isset($_SESSION['username'])) {
    header('Location: /login.php');
    exit();
}

if (!isset($_SESSION['final_score']) || !isset($_SESSION['final_questions_count'])) {
    header('Location: /');
    exit();
}

$final_score = $_SESSION['final_score'];
$final_questions_count = $_SESSION['final_questions_count'];

$percent = number_format(($final_score / $final_questions_count) * 100);

unset($_SESSION['final_score']);
unset($_SESSION['final_questions_count']);
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Results</title>
        <link rel="stylesheet" href="style.css">
        <script src="p5.min.js"></script>
        <script src="vanta.trunk.min.js"></script>
    </head>
    <body>
        <div class="content">
            <h2>Easy Quiz</h2>
            <p>Congratulations <?php echo htmlspecialchars($_SESSION['username']) ?>!</p>
            <p>You got <?php echo $final_score ?> right out of <?php echo $final_questions_count ?> which gives you a score of <?php echo $percent ?>%!</p>
<?php
if ($final_score === $final_questions_count) {
    $flag = file_get_contents('/flag.txt');
    echo "<p>You got a perfect score! Here is your flag: $flag</p>";
}
?>
            <p><a href="/">Go back</a></p>
        </div>
    </body>
</html>