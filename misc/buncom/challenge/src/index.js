import { $ } from "bun";

const src = "/tmp/custom.c", exe = "/tmp/a.out"

let hash = await $`
  cp default.c ${src};
  timeout 0.1 tcc ${src} -o ${exe};
  timeout 0.1 md5sum ${exe}`.text(), output = ""

const server = Bun.serve({
  host: "0.0.0.0",
  port: 1337,
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/") {
      const code = (new URLSearchParams(url.search)).get('code')
      if (code) {
        try {
          output = await $`echo ${code} > ${src}; timeout 0.1 tcc ${src} -o ${exe}`.text()
        } catch (err) {
          output = err.stderr.toString();
        }
      }
      if (await $`timeout 0.1 md5sum ${exe}`.text() !== hash) {
        await $`timeout 0.1 tcc default.c -o ${exe}`.text();
        output = `md5sum ${exe} != ` + hash;
      }
      let html = await $`${exe}`.text()
      html = html.replace('__CODE__', Bun.escapeHTML(await Bun.file(src).text()))
      return new Response(output + html, {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Content-Security-Policy": "script-src 'self'; object-src 'none'; base-uri 'none'; require-trusted-types-for 'script';"
        }
      });
    } else if (url.pathname === '/submit.js') {
      return new Response(await Bun.file('submit.js').text(), {
        headers: { 'Content-Type': 'application/javascript' },
      });
    }
  }
});

console.log(`listening on http://localhost:${server.port}`);
