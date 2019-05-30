const tf = require("@tensorflow/tfjs-node")
// testing
tf.setBackend("cpu")  
tf.enableDebugMode()
// end testing
const model = tf.loadLayersModel("file:///tmp/converted_model/model.json")


