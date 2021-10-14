let net;

let mymo;

async function app() {
  console.log("Loading mobilenet..");

  // Load the model.
  net = await mobilenet.load();
  console.log("Successfully loaded model");

  // mymodel
  mymo = await tf.loadLayersModel(
    "http://localhost:8000/model2000.s/model.json"
  );
  await mymo.compile({
    optimizer: tf.train.adam(),
    loss: "categoricalCrossentropy",
    metrics: ["accuracy"],
  });
  console.log("Successfully loaded my model");

  // Make a prediction through the model on our image.
  const imgEl = document.getElementById("img");
  const result = await net.classify(imgEl);
  const result21 = await mymo.classify(imgEl);
  console.log(result);
  console.log(result21);

  const imgEl2 = document.getElementById("img2");
  const result2 = await net.classify(imgEl2);
  const result22 = await mymo.classify(imgEl2);
  console.log(result2);
  console.log(result22);
}

app();
