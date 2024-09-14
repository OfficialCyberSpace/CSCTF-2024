# key

The solution for this problem is to reverse the rudimentary mathematical operation preformed on the key that is then checked agianst the obfuscated key. Another solution would be to brute force each character individually as each character is done one at a time.

My solution was the brute force script, as I had already created it from other CTF events, however it would probably be easier with no prior tools to crack the simble math behind the problem.
Yes, it can be improved and made faster in this implementation but it wasn't changed much since the last implementation.

> Note, my solution only works some of the time due to ASLR. The location of i in the for loop, which I check if it increments may be offset more or less from that position in memory. You can check that in gdb, and then switch the script accordingly.
