.PHONY: setup submodules

setup: submodules
>>>>>>> ee42e82 (lazy: had old targets in Makefile)

submodules:
	git submodule init
	git submodule update

model: # needs retrain.py or sth else to fetch keras before
	cd meta/node-tfjs-retrain/ && node app.js --images_dir="~/keras/datasets/flower_photos/" --model_dir="../../model-flowers-gls-only"

find_alpha_pics:
	identify -format '%f %[channels]\n' images/plaintext/*/* | grep rgba

