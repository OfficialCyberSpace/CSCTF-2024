# silly-camel

In Perl, you can create a function from a string by doing something like `$fn = *{"function_name_here"}`, so we can use this to create any function. In most cases, creating functions like this will not allow you to use "unsafe" functions like `system`, but for some reason it allows `CORE::evalbytes` which works exactly the same as `eval`, so we can so something like `*{"CORE::evalbytes"}->("code here")` to execute arbitrary code. To generate the actual strings for this challenge, we can use `<str here>` to make arbitrary strings (there's a weird set of rules you have to follow for it to work properly, but won't go in depth for this short writeup), and then xor it with another string to form our desired string.

In the end, I went with `*{"CORE::evalbytes"}->("exec('/readflag')")`.

Which results in this payload:

```
*{<!!!!!!!!(!!(!!!>^<=0,:##8)51=-)8,>^<_^_^88|~||~|||~>}->(<!(!(!!!!!(!!!(!!!>^<8,850(#-8599158(#>^<|||~9.-~|||~||~.+>)
```

Refer to solve in [solve.py](./solve.py) to see how I set up the payload.
