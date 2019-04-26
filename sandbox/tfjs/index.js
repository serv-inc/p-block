let net;

const classifier = knnClassifier.create();

// todo: refactor
async function addA() {
  // get image data, add to class a
  const activation = net.infer(imageElement, 'conv_preds');
  classifier.addExample(activation, 0);
}

async function addB() {
  // get image data, add to class B
}

async function app() {
  console.log('Loading mobilenet..');

  // Load the model.
  net = await mobilenet.load();
  console.log('Sucessfully loaded model');

  const addExample = classId => {
    // Get the intermediate activation of MobileNet 'conv_preds' and pass that
    // to the KNN classifier.
    const activation = net.infer(webcamElement, 'conv_preds');

    // Pass the intermediate activation to the classifier.
    classifier.addExample(activation, classId);
  };

  // Make a prediction through the model on our image.
  const imgEl = document.getElementById('img');
  const result = await net.classify(imgEl);
  console.log(result);
}

app();
