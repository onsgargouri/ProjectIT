// Function to send user input to the Python code for evaluation
function evaluatePassword() {
  var password = document.getElementById("password").value;

  // Create a new FormData object
  var formData = new FormData();
  formData.append("password", password);

  // Send a POST request to the Python code using fetch API
  fetch("/evaluate-password", {
    method: "POST",
    body: formData,
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // Handle the response from the Python code
      var score = data.score;
      var evaluation = data.evaluation;
      var feedback = data.feedback;

      // Display the result to the user
      document.getElementById("score").textContent = "Password Score: " + score;
      document.getElementById("evaluation").textContent = "Evaluation: " + evaluation;
      document.getElementById("feedback").textContent = "Feedback: " + feedback;
    })

    });
}



function toggle(){
    let password = document.getElementById("password");
    let eye = document.getElementById("toggle");

    if(password.getAttribute("type") == "password"){
        password.setAttribute("type","text");
        eye.style.color = "#0be881";
    }
    else{
        password.setAttribute("type","password");
        eye.style.color = "#808080";
    }
}
