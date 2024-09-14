<!DOCTYPE html>
<html>
<head>
    <title>Twig Playground</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 80%;
            max-width: 800px;
            margin: 20px auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-top: 200px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        .output {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 4px;
            background: #fafafa;
        }
        .error {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Twig Playground</h1>
        <form method="post" action="">
            <label for="input">Enter Twig Expression:</label>
            <input type="text" id="input" name="input" placeholder="{{ user.name }} is {{ user.age }} years old."><br>
            <input type="submit" value="Render">
        </form>

        <?php
        ini_set('display_errors', 0);
        ini_set('error_reporting', 0);
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            require_once 'vendor/autoload.php';

            $loader = new \Twig\Loader\ArrayLoader([]);
            $twig = new \Twig\Environment($loader, [
                'debug' => true,
            ]);
            $twig->addExtension(new \Twig\Extension\DebugExtension());

            $context = [
                'user' => [
                    'name' => 'Wesley',
                    'age' => 30,
                ],
                'items' => ['Apple', 'Banana', 'Cherry', 'Dragonfruit'],
            ];

            // Ensure no SSTI or RCE vulnerabilities
            $blacklist = ['system', 'id', 'passthru', 'exec', 'shell_exec', 'popen', 'proc_open', 'pcntl_exec', '_self', 'reduce', 'env', 'sort', 'map', 'filter', 'replace', 'encoding', 'include', 'file', 'run', 'Closure', 'Callable', 'Process', 'Symfony', '\'', '"', '.', ';', '[', ']', '\\', '/', '-'];

            $templateContent = $_POST['input'] ?? '';

            foreach ($blacklist as $item) {
                if (stripos($templateContent, $item) !== false) {
                    die("Error: The input contains forbidden content: '$item'");
                }
            }

            try {
                $template = $twig->createTemplate($templateContent);

                $result = $template->render($context);
                echo '<h2>Rendered Output:</h2>';
                echo '<div class="output">';
                echo htmlspecialchars($result);  // Ensure no XSS vulnerabilities
                echo '</div>';
            } catch(Exception $e) {
                echo '<div class="error">Something went wrong! Try again.</div>';
            }
        }
        ?>
    </div>
</body>
</html>
