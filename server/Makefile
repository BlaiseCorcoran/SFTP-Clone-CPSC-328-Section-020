all: fileserver

fileserver: server.py
	cp server.py fileserver
	chmod u+x fileserver

clean:
	rm -rf fileserver
	rm -rf __pycache__

.PHONY: clean