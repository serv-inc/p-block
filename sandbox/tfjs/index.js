let net;

async function app() {
  console.log('Loading model.');

  // Load the model.
  const model = await tf.loadLayersModel("http://127.0.0.1:9090/model.json");
  console.log('Sucessfully loaded model');

  const imgEl = document.getElementById('img');
  const result = await model.classify(imgEl);
  console.log(result);
}

app();
