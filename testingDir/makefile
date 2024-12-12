all: fileserver fileclient

fileserver: server.py
	cp server.py fileserver
	chmod u+x fileserver

fileclient: client.py
	cp client.py fileclient
	chmod u+x fileclient

clean:
	rm -rf fileserver
	rm -rf fileclient
	rm -rf __pycache__

.PHONY: clean