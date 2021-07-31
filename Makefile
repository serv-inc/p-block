.PHONY: all mountcrypt retrain submodules encrypted_zip train clean

all: mountcrypt

setup: submodules
	git lfs fetch
	git lfs checkout

retrain: /tmp/example_code/retrain.py # images in tmp/test
	cd /tmp && mkdir example_code && cd example_code
	curl -LO https://github.com/tensorflow/hub/raw/master/examples/image_retraining/retrain.py
	python /tmp/example_code/retrain.py --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 --image_dir /tmp/test
	tensorflowjs_converter --input_format=tf_frozen_model --output_node_names='final_result' --output_json=true /tmp/output_graph.pb /tmp/my_model  # needs version 0.8.5

submodules:
	git submodule init
	git submodule update

model_gls:
	cd meta/node-tfjs-retrain/ && node app.js --images_dir="../../../../.keras/datasets/flower_photos/" --model_dir="../../model-flowers-gls-only"

train: submodules
	cd meta/node-tfjs-retrain/ && make train

smaller:
	cd images/plaintext && for i in $(ls); do (cd $i; optipng -snip *gif && rm *gif); done

clean:
	rm -rf V
