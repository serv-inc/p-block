all: mountcrypt

mountcrypt: images/plaintext images/cipher
	cd images && gocryptfs cipher/ plaintext/

images/plaintext:
	mkdir images/plaintext

# needs gocryptfs to be loaded once
tmp/test:
	mkdir -p /tmp/test
	cp -r images/plaintext/nopns/ images/plaintext/somepns/ images/challenge2018/ /tmp/test

retrain: /tmp/test
	curl -LO https://github.com/tensorflow/hub/raw/master/examples/image_retraining/retrain.py
	python retrain.py --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 --image_dir /tmp/test
