# Share The Flag

- Notice how discord shows an embed for shared files

  - Discord's bot only looks for meta tags in the html response, not rendering any JS
  - The site's meta tags are only visible once react injects them into the page, not being present in the initial HTML response (present while inspecting the page, but not in the view-source: page)
  - How can discord know the meta tags without rendering JS? The response the discord bot is getting must be different from what normal users see.
  - If we set up a webhook and send it in a discord chat, we will get a request from discord's bot, and we realise discord sends a custom user agent to our webhook.
  - We can try requesting a cybersharing page with discord's user-agent and we will get an already fully rendered html page as the response. containing not only meta tags but also the html body content, instead of the usual minimal html content.
  - We can only assume the JS is being rendered in the server, possibly in a headless browser and sent to social media bots

- Et3rnos mentions that 0xM4hm0ud is supposed to be able to access the file if he connects to his home vpn
  - This hints to the fact that the file was shared with the "Save To IP History" option enabled, that makes files discoverable to everyone that shares the same IP by visiting https://cybersharing.net/history
  - He mentions that he mistakenly uploaded it while connected to the cybersharing vpn instead, so it is safe to assume that the file is now only accessible to requests from inside cybersharing's server
- Since we can render page responses in the server by using discordbot's user agent, we can request the ip history page with discord's user agent, which will return the list of files uploaded by the server's ip
  - `curl https://cybersharing.net/history -H "User-Agent: discordbot"`
  - We notice a file flag.txt in the response, with a href of `/s/13f17b167f2229809a95fb9d8c725449`
  - By visiting https://cybersharing.net/s/13f17b167f2229809a95fb9d8c725449 we get the flag

For a detailed and in-depth explanation of the "Share The Flag" challenge, you can refer to the write-up available on LearnCyber. It walks through the different steps of the challenge.
You can find the full write-up [here](https://learn-cyber.net/writeup/Share-The-Flag).
