
# Honestly this did not need a Makefile but wtv :sob:

CC = gcc
DEBUG_FLAGS = -g
RELEASE_FLAGS = -O3 -s -w
TARGET = vmvm

.PHONY: build debug

build:
	$(CC) $(RELEASE_FLAGS) -o $(TARGET) vm.c

debug:
	$(CC) $(DEBUG_FLAGS) -o $(TARGET) vm.c