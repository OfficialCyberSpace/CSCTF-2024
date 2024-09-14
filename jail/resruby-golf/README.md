# resruby golf

Find intended writeup [here](../resruby/README.md)

Made this during the CTF because some people figured out how to create empty strings given the restrictions. The empty string was then used
in combination with the shovel operator to form the "flag.txt" string. Clever, but not what I wanted people to use </3

Example:

```rb
%() << 102 << 108 << 97 << # ... etc etc
```
