all: testLib

testLib:
	cp test.py testLib
	chmod u+x testLib

clean:
	rm -rf testLib
	rm -rf __pycache__

.PHONY: clean