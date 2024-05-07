const imgArea = document.querySelector(".img-area");
const inputFile = document.getElementById("file");
document.getElementById("sendButton").addEventListener("click", function () {
  console.log("Button clicked"); // Add this line for debugging
  const imageFile = inputFile.files[0];
  if (imageFile) {
    sendToFlaskAPI(imageFile);
  } else {
    alert("Please select an image before sending to API");
  }
});
document.getElementById("selectImage").addEventListener("click", function () {
  inputFile.click();
});

document.getElementById("file").addEventListener("change", function () {
  const image = this.files[0];
  if (image) {
    if (image.size < 2000000) {
      const reader = new FileReader();
      reader.onload = () => {
        const allImg = imgArea.querySelectorAll("img");
        allImg.forEach((item) => item.remove());
        const imgUrl = reader.result;
        const img = document.createElement("img");
        img.src = imgUrl;
        imgArea.appendChild(img);
        imgArea.classList.add("active");
        imgArea.dataset.img = image.name;
      };
      reader.readAsDataURL(image);
    } else {
      alert("Image size more than 2MB");
    }
  } else {
    alert("Please select an image file");
  }
});

// Function to send image and first name to Flask API
function sendToFlaskAPI(imageFile) {
  const formData = new FormData();
  formData.append("image", imageFile);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/predict", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const predictedCategory = xhr.responseText;
      var response = JSON.parse(predictedCategory);
      var result = document.getElementById("result");
      result.innerHTML =
        "<strong>predicted Category:</strong>" + response["predicted_category"];
      console.log(xhr.responseText); // Contains the response body
    }
  };
  xhr.send(formData);
}

// validation on submit
document.getElementById("registrationForm").onsubmit = function (e) {
  firstNameValidation();
  if (firstNameValidation() == true) {
    return true;
  } else {
    return false;
  }
};
