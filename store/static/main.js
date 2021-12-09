"use strict";

let orderInfo = {
  door_finish: "Unpainted",
  glass: "Glass 1",
  door_width: "30",
  door_height: "6'8\"",
};

const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
canvas.width = 450;
canvas.height = 900;

const defaultImg = new Image(450, 900);
defaultImg.onload = function () {
  context.drawImage(defaultImg, 0, 0);
};
defaultImg.src = "/static/images/unpainted.png";
let bcgImg = defaultImg.src;

function displayImg() {
  let newImg = new Image(450, 900);
  newImg.onload = function () {
    context.drawImage(newImg, 0, 0);
  };
  newImg.src = this.attributes["data-img"].value;
  bcgImg = newImg;
}

function combineImg() {
  const img1 = new Image(450, 900);
  img1.src = this.attributes["data-img"].value;
  const img2 = new Image(450, 900);
  img2.src = bcgImg;

  img1.onload = function () {
    context.drawImage(img1, 0, 0);
  };
  context.globalAlpha = 1.0;
  context.drawImage(img1, 0, 0);
  context.drawImage(img2, 0, 0);
}

// Paints
document.getElementById("unpainted").addEventListener("change", displayImg);
document.getElementById("unpainted").addEventListener("change", function () {
  orderInfo.door_finish = "Unpainted";
});

document.getElementById("paint").addEventListener("change", displayImg);
document.getElementById("paint").addEventListener("change", function () {
  orderInfo.door_finish = "Paint";
});

document.getElementById("stain").addEventListener("change", displayImg);
document.getElementById("stain").addEventListener("change", function () {
  orderInfo.door_finish = "Stain";
});

// Glasses
document.getElementById("glass_1").addEventListener("change", combineImg);
document.getElementById("glass_1").addEventListener("change", function () {
  orderInfo.glass = "Glass 1";
});

document.getElementById("glass_2").addEventListener("change", combineImg);
document.getElementById("glass_2").addEventListener("change", function () {
  orderInfo.glass = "Glass 2";
});

document.getElementById("glass_3").addEventListener("change", combineImg);
document.getElementById("glass_3").addEventListener("change", function () {
  orderInfo.glass = "Glass 3";
});

// Width
document.getElementById("width-30").addEventListener("change", function () {
  orderInfo.door_width = "30";
});

document.getElementById("width-32").addEventListener("change", function () {
  orderInfo.door_width = "32";
});

document.getElementById("width-34").addEventListener("change", function () {
  orderInfo.door_width = "34";
});
document.getElementById("width-36").addEventListener("change", function () {
  orderInfo.door_width = "36";
});

// Height
document.getElementById("height-6_8").addEventListener("change", function () {
  orderInfo.door_height = "6'8\"";
});

document.getElementById("height-8").addEventListener("change", function () {
  orderInfo.door_height = "8'";
});

document
  .getElementById("submit_button")
  .addEventListener("click", sendOrderInfo);

function sendOrderInfo() {
  let req = new XMLHttpRequest();
  req.open("POST", "/products");
  req.setRequestHeader("Content-Type", "application/json");
  req.onload = () => {
    console.log(req.response);
  };
  req.send(JSON.stringify(orderInfo));
}
