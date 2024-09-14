<?php
session_start();
require_once "config.php";

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (!isset($_GET['topic'])) {
        header('Location: /');
        exit();
    }

    $quizzes = json_decode(file_get_contents('./quizzes.json'), true);

    $topic = $_GET['topic'];
    $q_num = 0;
    $correct = 0;
    $next_correct = rand(0, count($quizzes[$topic][$q_num]['answers'])-1);

    if (!isset($quizzes[$topic])) {
        header('Location: /');
        exit();
    }

    $question = $quizzes[$topic][$q_num]['question'];
    $answers = $quizzes[$topic][$q_num]['answers'];
    $message = "Good luck!";

    $_SESSION['topic'] = $topic;
    $_SESSION['q_num'] = $q_num;
    $_SESSION['correct'] = $correct;
    $_SESSION['next_correct'] = $next_correct;
}
elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_SESSION['topic'], $_SESSION['q_num'], $_SESSION['correct'], $_SESSION['next_correct'])) {
        header('Location: /');
        exit();
    }

    $topic = $_SESSION['topic'];
    $q_num = $_SESSION['q_num'];
    $correct = $_SESSION['correct'];
    $next_correct = $_SESSION['next_correct'];

    $quizzes = json_decode(file_get_contents('./quizzes.json'), true);

    if (!isset($quizzes[$topic])) {
        header('Location: /');
        exit();
    }

    $answer = $_POST['answer'];

    if (intval($answer) === $next_correct) {
        $message = "Good job " . htmlspecialchars($_SESSION['username']) . ", that was correct!";
        $correct++;
    }
    else {
        $message = "Sorry " . htmlspecialchars($_SESSION['username']) . ", that's not right...";
    }
    $q_num++;

    if ($q_num < count($quizzes[$topic])) {
        $question = $quizzes[$topic][$q_num]['question'];
        $answers = $quizzes[$topic][$q_num]['answers'];
        $next_correct = rand(0, count($quizzes[$topic][$q_num]['answers'])-1);
        $_SESSION['q_num'] = $q_num;
        $_SESSION['correct'] = $correct;
        $_SESSION['next_correct'] = $next_correct;
    } else {
        $_SESSION['final_score'] = $correct;
        $_SESSION['final_questions_count'] = count($quizzes[$topic]);

        unset($_SESSION['topic'], $_SESSION['q_num'], $_SESSION['correct']);

        header('Location: /result.php');
        exit();
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Easy Quiz - <?php $topic ?></title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="content">
            <h2>Easy Quiz - <?php echo $topic ?></h2>
            <p><?php echo $message ?></p>
            <p>Question #<?php echo $q_num+1 ?>:</p>
            <p><?php echo $question ?></p>
            <form method="POST" action="quiz.php">
                <?php foreach ($answers as $key => $value): ?>
                    <input type="radio" name="answer" value="<?php echo $key ?>" required>
                    <?php echo $value ?><br>
                <?php endforeach; ?>
                <button type="submit">Next</button>
            </form>
            <p><a href="index.php">Exit Quiz</a></p>
        </div>
    </body>
</html>
