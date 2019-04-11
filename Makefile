images/plaintext:
	mkdir images/plaintext

crypt: images/plaintext images/cipher
	cd images && gocryptfs cipher/ plaintext/
