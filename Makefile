all: mountcrypt

mountcrypt: images/plaintext images/cipher
	cd images && gocryptfs cipher/ plaintext/

images/plaintext:
	mkdir images/plaintext

# needs gocryptfs to be loaded once
tmp/test:
	mkdir -p /tmp/test
	cp -r images/plaintext/nopns/ images/plaintext/somepns/ images/challenge2018/ /tmp/test
