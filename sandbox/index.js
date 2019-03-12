var canvasA = document.getElementById("canvasA");
var canvasB = document.getElementById("canvasB");
var canvasC = document.getElementById("canvasC");
var canvasD = document.getElementById("canvasD");
var canvasE = document.getElementById("canvasE");
var canvasF = document.getElementById("canvasF");
var image = new MarvinImage();
var imageOut = new MarvinImage();


image.load("./picture.jpg", function(){
  Marvin.scale(image, imageOut, 300, 156);
  imageOut.draw(canvasA);
  Marvin.crop(image, imageOut, 0, 0, 300, 156);
  imageOut.draw(canvasB);
  Marvin.crop(image, imageOut, 0, image.getHeight()/2, 300, 156);
  imageOut.draw(canvasC);  
  Marvin.crop(image, imageOut, image.getWidth()/2, 0, 300, 156);
  imageOut.draw(canvasD);  
  Marvin.crop(image, imageOut, image.getWidth()/2, image.getHeight()/2, 300, 156);
  imageOut.draw(canvasE);
  Marvin.crop(image, imageOut, image.getWidth()/4, image.getHeight()/4, 300, 156);
  imageOut.draw(canvasF);  
});
