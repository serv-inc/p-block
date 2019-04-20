all: mountcrypt

mountcrypt: images/plaintext images/cipher
	cd images && gocryptfs cipher/ plaintext/

images/plaintext:
	mkdir images/plaintext


tmp/test:
	mkdir /tmp/test
	cp -r images/plaintext/nopns/ images/plaintext/somepns/ images/challenge2018/ /tmp/test
