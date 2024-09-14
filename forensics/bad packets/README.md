# bad packets

- The packet capture shows tampering of `oldcss` via Trevor C2.
- Trevor C2 is a command-and-control framework (details [here](https://nasbench.medium.com/understanding-detecting-c2-frameworks-trevorc2-2a9ce6f1f425)).
- Use the `trevorc2_server.py` script from the TrevorC2 repository ([link](https://github.com/trustedsec/trevorc2/blob/master/trevorc2_server.py)).
- Decrypt one of the `oldcss` values in the TCP stream.
- Use the same AES key from the encryption process to get the flag.

Refer to [solve.py](solve.py) for the solution.
