.PHONY: all mountcrypt retrain submodules encrypted_zip	

all: mountcrypt

setup: submodules
	git lfs fetch
	git lfs checkout

mountcrypt: images/plaintext images/cipher
	cd images && gocryptfs -q cipher/ plaintext/

images/plaintext:
	mkdir images/plaintext

# needs gocryptfs to be loaded once
tmp/test:
	mkdir -p /tmp/test
	cp -r images/plaintext/nopns/ images/plaintext/somepns/ images/challenge2018/ /tmp/test

/tmp/example_code/retrain.py:
	mkdir /tmp/example_code
	cd /tmp/example_code && wget https://github.com/tensorflow/hub/raw/master/examples/image_retraining/retrain.py

retrain: /tmp/example_code/retrain.py # images in tmp/test
	curl -LO https://github.com/tensorflow/hub/raw/master/examples/image_retraining/retrain.py
	python /tmp/example_code/retrain.py --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 --image_dir /tmp/test
	tensorflowjs_converter --input_format=tf_frozen_model --output_node_names='final_result' --output_json=true /tmp/output_graph.pb /tmp/my_model  # needs version 0.8.5

submodules:
	git submodule init
	git submodule update

encrypted_zip: images/plaintext
	zip --encrypt -r images/does.zip images/plaintext/somepns/
	zip --encrypt -r images/no.zip images/plaintext/nopns/

decrypt_zip: images/does.zip images/no.zip
	unzip images/no.zip 
	unzip images/does.zip 
