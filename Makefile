all: mountcrypt

mountcrypt: images/plaintext images/cipher
	cd images && gocryptfs cipher/ plaintext/

images/plaintext:
	mkdir images/plaintext

