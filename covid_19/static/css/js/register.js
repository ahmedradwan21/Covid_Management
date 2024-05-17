// First Name Validation
var fname = document.getElementById("firstname");
var fnameValidation = function () {
  fnameValue = fname.value.trim();
  validFname = /^[A-Za-z]+[A-Za-z]+$/;
  var fnameError = document.getElementById("fname_error");
  if (fnameValue == "") {
    fnameError.innerHTML = "**First Name is required";
  } else if (!validFname.test(fnameValue)) {
    fnameError.innerHTML = "**Invalid Name";
  } else {
    fnameError.innerHTML = "";
    return true;
  }
};
fname.oninput = function () {
  fnameValidation();
};

// Last Name Validation
var lname = document.getElementById("lastname");
var lnameValidation = function () {
  lnameValue = lname.value.trim();
  validLname = /^[A-Za-z]+[A-Za-z]+$/;
  var lnameError = document.getElementById("lname_error");
  if (lnameValue == "") {
    lnameError.innerHTML = "**Last Name is required";
  } else if (!validLname.test(lnameValue)) {
    lnameError.innerHTML = "**Invalid Name";
  } else {
    lnameError.innerHTML = "";
    return true;
  }
};
lname.oninput = function () {
  lnameValidation();
};

// Mobile Number Validation
var phonenum = document.getElementById("phone");
var phonenumValidation = function () {
  phonenumValue = phonenum.value.trim();
  validPhonenum = /^[0-9]*$/;
  var phonenumError = document.getElementById("phone_error");
  if (phonenumValue == "") {
    phonenumError.innerHTML = "**Phone Number is required";
  } else if (!validPhonenum.test(phonenumValue)) {
    phonenumError.innerHTML = "**Phone Number must be a number";
  } else if (phonenumValue.length != 11) {
    phonenumError.innerHTML = "**Phone Number must have 11 digits";
  } else {
    phonenumError.innerHTML = "";
    return true;
  }
};
phonenum.oninput = function () {
  phonenumValidation();
};

// Email Address Validation
var email = document.getElementById("email");
var emailValidation = function () {
  emailValue = email.value.trim();
  validEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  var emailError = document.getElementById("email_error");
  if (emailValue == "") {
    emailError.innerHTML = "**Email Address is required";
  } else if (!validEmail.test(emailValue)) {
    emailError.innerHTML = "**Invalid Email Address";
  } else {
    emailError.innerHTML = "";
    return true;
  }
};
email.oninput = function () {
  emailValidation();
};
// Password Validation
var pwd = document.getElementById("pwd");
var pwdValidation = function () {
  pwdValue = pwd.value.trim();
  validPwd =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  var pwdError = document.getElementById("pwd_error");
  if (pwdValue == "") {
    pwdError.innerHTML = "**Password is required";
  } else if (!validPwd.test(pwdValue)) {
    pwdError.innerHTML =
      "**Password must have at least one uppercase, lowercase, digit, special character & 8 characters";
  } else {
    pwdError.innerHTML = "";
    return true;
  }
};
pwd.oninput = function () {
  pwdValidation();
  confirmValidation();
};
// Confirm Password Validation
var confirm = document.getElementById("confirm");
var confirmValidation = function () {
  confirmValue = confirm.value.trim();

  var confirmError = document.getElementById("confirm_error");
  if (confirmValue == "") {
    confirmError.innerHTML = "**Confirm Password is required";
  } else if (confirmValue != pwd.value) {
    confirmError.innerHTML = "**Confirm Password does not match";
  } else {
    confirmError.innerHTML = "";
    return true;
  }
};
confirm.oninput = function () {
  confirmValidation();
};
// validation on submit
document.getElementById("registrationForm").onsubmit = function (e) {
  fnameValidation();
  lnameValidation();
  phonenumValidation();
  emailValidation();
  pwdValidation();
  confirmValidation();
  if (
    fnameValidation() == true &&
    lnameValidation() == true &&
    phonenumValidation() == true &&
    emailValidation() == true &&
    pwdValidation() == true &&
    confirmValidation() == true
  ) {
    return true;
  } else {
    return false;
  }
};