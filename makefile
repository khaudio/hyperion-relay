CC := g++
DEBUG := -g
CFLAGS := -std=c++11
LFLAGS := -Wall -lwiringPi
SOURCEDIR := src
SOURCES := $(shell find $(SOURCEDIR) -name 'hyperion_relay.cpp')
BINARY := hyperion_relay.out

.PHONY: clean

p1:
	$(CC) $(CFLAGS) $(SOURCES) -o $(BINARY)

p2:
	$(CC) $(LFLAGS) $(CFLAGS) $(SOURCES) $(DEBUG) -o $(BINARY)

all: p1

debug: p2

run: all
	./$(BINARY)

clean:
	\rm ./$(BINARY)

distclean: clean