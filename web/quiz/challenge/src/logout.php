<?php
session_start();
require_once 'config.php';
unset($_SESSION['username']);
header('Location: /login.php');
?>