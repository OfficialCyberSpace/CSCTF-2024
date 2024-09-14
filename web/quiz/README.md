# Quiz

#### Author: GabeG888

## Description

Just 25 simple questions. Can you get a perfect score?

## Writeup

The /logout.php endpoint only removes the username variable from your session, it doesn't completely destroy it. Unlike all the other endpoints, /quiz.php does not redirect to /login.php if $\_SESSION['username'] is not set. This allows you to answer quiz questions after logging out. However, the code tries to access $\_SESSION['username'] to print out a message, which causes an error if you have logged out. A custom error handler is set in config.php so that execution is halted when there is an error. By making requests to /quiz.php while logged out, you can learn the correct answer to the next question by guessing all five options and watching the line number of the error when accessing the username. The error is on a different line if the guess was correct. After you know the correct answer, you can log back in and submit it. Repeat this process for all 25 questions.
