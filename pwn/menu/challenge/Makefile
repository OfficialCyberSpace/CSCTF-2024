CC := gcc
CFLAGS := -fno-stack-protector -Wl,-z,relro,-z,now -w
LFLAGS := -lseccomp

chal: chal.c
	$(CC) $(CFLAGS) $< -o $@ $(LFLAGS)

clean:
	rm -f chal