#include <stdio.h>

int main() {
  #define R(...) #__VA_ARGS__
  printf(R(
    <!DOCTYPE html>
    <html lang='en'>
    <head>
      <meta charset='UTF-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1.0'>
      <title>Crack the hash, keep the website</title>
      <style>
      body {
        font-family: Arial, sans-serif;
      }
      .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      textarea {
        width: 100%;
        height: 200px;
        font-family: monospace;
        font-size: 14px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      button {
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #007BFF;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }
      button:hover {
        background-color: #0056b3;
      }
      </style>
    </head>
    <body>
      <div class='container'>
      <h1>Crack the hash, keep the website</h1>

      <form id='codeForm'>
        <textarea id='codeInput'>__CODE__</textarea>
        <button type='submit'>Submit</button>
      </form>
      </div>

      <script src="submit.js"></script>
    </body>
    </html>
  ));
}
