# cipher block clock

IV and key are improperly used. IV and key are swapped to where the IV is reused between the two messages and keys are known.

To find the IV, decrypt the message with the key with the IV of `00000000000000000000000000000000` to obtain the decrypted but not XOR'ed first block of the message. XOR the first block with the plain text to obtain the IV. Afterwards, decrypt the message for flag with IV and key with the second cipher text.

```
pt = D(k, ct) XOR IV
ct = E(k, (pt XOR IV))
```

- [Step 1](<https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'Hex','string':'667a704a5b4730f1954692ea0d924a7f9ea8fe478415fa2aad8ae59604f7950e'%7D,%7B'option':'Hex','string':'00000000000000000000000000000000'%7D,'CBC','Hex','Hex',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=NjU3MGY1ZjliOGM0M2E2NjIyYjFiNGFiYzAzN2ZhMDljZDgyYmUxNTcwZWMxZjI2MjUzOGVmZjE3Mzc0MTYxNjczMjc2Y2I4MjMwNDY3NmY3YTM3YjY1OGFlOWM5OTdlNmM1YjE3OTg3OTI4ZjJkZDI5MmNjN2VjMmZjYzZiOWVkMjI5OTQ2MTY4NDhlZTcxNmJjZjYxNDJlMDY4OWIzYWExYzVhYmJjZDNjMzE2YTMzMjlmOGY1MWYzNzhjZjZlMTBjYmVlZWZlNTRhMzYxMWRjODc4ZDIzYzYwNmU3OGUxMTRkYTY4MTZmYTM4NDYwNWY3NWYyNjI5OWExZDlkY2E4M2RlZDIzYjFmN2NkZDFlOGFjY2VkNmZjYjE5OWZkYTM0YTNiYzI2ZDJlODhiYzNjZTAxNDY2YTc0ZTQ0NzQ0ZTVhMGU2NWNhYjI1NzQ1YzY0ZjE3OGNkNzY4MGUyYjNjOTkzMjg2ZTIzNmNkM2M1NWUyMmNkZDcxYWFjMjc5Yzc0OWRkY2Y0ZjgxMzc4NjdiNjgyYzI5ZjEwZDc1NGRhNGY2YjIyNjAzNTMxYTQ4ODVhNTE0NGYwMTJjOGYyMw>)

- [Step 2](<https://gchq.github.io/CyberChef/#recipe=XOR(%7B'option':'Hex','string':'b092893dfd9d2e73b2d6ee83413f8c52'%7D,'Standard',false)To_Hex('None',0)&input=TG9va2llIGhlcmUsIHNvbQ&oeol=VT>)

- [Step 3](<https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'Hex','string':'667a704a5b4730f1954692ea0d924a7f9ea8fe478415fa2aad8ae59604f7950e'%7D,%7B'option':'Hex','string':'fcfde65694f80e1bd7a48baf614ce33f'%7D,'CBC','Hex','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=NjU3MGY1ZjliOGM0M2E2NjIyYjFiNGFiYzAzN2ZhMDljZDgyYmUxNTcwZWMxZjI2MjUzOGVmZjE3Mzc0MTYxNjczMjc2Y2I4MjMwNDY3NmY3YTM3YjY1OGFlOWM5OTdlNmM1YjE3OTg3OTI4ZjJkZDI5MmNjN2VjMmZjYzZiOWVkMjI5OTQ2MTY4NDhlZTcxNmJjZjYxNDJlMDY4OWIzYWExYzVhYmJjZDNjMzE2YTMzMjlmOGY1MWYzNzhjZjZlMTBjYmVlZWZlNTRhMzYxMWRjODc4ZDIzYzYwNmU3OGUxMTRkYTY4MTZmYTM4NDYwNWY3NWYyNjI5OWExZDlkY2E4M2RlZDIzYjFmN2NkZDFlOGFjY2VkNmZjYjE5OWZkYTM0YTNiYzI2ZDJlODhiYzNjZTAxNDY2YTc0ZTQ0NzQ0ZTVhMGU2NWNhYjI1NzQ1YzY0ZjE3OGNkNzY4MGUyYjNjOTkzMjg2ZTIzNmNkM2M1NWUyMmNkZDcxYWFjMjc5Yzc0OWRkY2Y0ZjgxMzc4NjdiNjgyYzI5ZjEwZDc1NGRhNGY2YjIyNjAzNTMxYTQ4ODVhNTE0NGYwMTJjOGYyMw>)

- [Step 4](<https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'Hex','string':'b800f4bfd38030ff3ed82560a11e9ef67e9c3529ab52938c9458c7d8602d7a51'%7D,%7B'option':'Hex','string':'fcfde65694f80e1bd7a48baf614ce33f'%7D,'CBC','Hex','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=NWFiYjg0OTBkODcyZjEwMWRjZDg5YWY0MjE5NThjNTQyMDQ2NDJlN2QwZjk2YTYzOTM3NTlmNDVjOTYzMGU5YjZiMTZlODdlOWE5NmQwMDA0NGZlZDI4ZTI5NTE2M2M1ZmM2ZWQyYTU5ODM5YzRiZTQzM2Y3NGY4NjE0ZmNlNTQ>)
