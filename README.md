- `-> Discord Token`
0. Open Discord Web in a browser
1. Press F12 (Developer Tools)
2. Go to Network -> Name(access-token) -> authorization (copy the value of token) https://github.com/ROSTGG/discord-chat-import/blob/main/image.png
3. WARNING The token gives full account access. Never share it.

- `-> Channel ID`
0. Go to your User Settings in your Discord client. On Desktop, you can access User Settings by clicking on the cogwheel icon near the bottom-left, next to your username.
1. Click on Advanced tab from the left-hand sidebar and toggle on Developer Mode.
2. Right-click the channel → Copy Channel ID.

- `-> Run python script`
Past Discord Token, Channel ID and enter format(txt, json)

- `txt Example` 
* [2026-01-09T18:41:12.000Z] UserA: Hello
* [2026-01-09T18:41:40.000Z] UserB: How are you?
*   ↳ reply to: Hello
*   [reactions: 👍×2]

- `JSON includes`
timestamp, author, content, reply text (if exists), reactions, mentions, attachment URLs
