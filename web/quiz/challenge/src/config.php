<?php
set_error_handler(function($errno, $errstr, $errfile, $errline) {
    if (error_reporting() & $errno) {
        echo "Error: [$errno] $errstr - $errfile:$errline\n";
    }
    exit(1);
});

$dsn = "sqlite:/home/user/db/quiz.db";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

$pdo = new PDO($dsn, null, null, $options);
?>
