const tf = require("@tensorflow/tfjs-node")
//const fs = require("fs")

const sharp = require("sharp")
// testing
tf.setBackend("cpu")  
tf.enableDebugMode()
// end testing
const model = tf.loadLayersModel("file:///tmp/converted_model/model.json")
// sharp("/tmp/test/nopns/x91.jpg").resize(224, 224)

