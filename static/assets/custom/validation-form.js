/*
function checkEmail() {
    var email = document.getElementById("email");
	var buttonRegister = document.getElementById("buttonRegister");
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email.value)) {
      email.style.border = "3px solid red";
	  buttonRegister.disabled = true;
    } else {
      email.style.border = "3px solid green";
	  buttonRegister.disabled = false;
    }
}
function checkUsername() {
    var username = document.getElementById("username");
	var buttonRegister = document.getElementById("buttonRegister");

    if (username.value.length < 6) {
		username.style.border = "3px solid red";
		buttonRegister.disabled = true;
    } else {
		username.style.border = "3px solid green";
		buttonRegister.disabled = false;
    }
	
	if (username.value === "") {
		username.style.border = "none";
	}
}

function comparePassword() {
	var password = document.getElementById("password");
	var repeatPassword = document.getElementById("repeatPassword");
	var buttonRegister = document.getElementById("buttonRegister");
	
	if(password.value !== repeatPassword.value) {
		password.style.border = "3px solid red";
		repeatPassword.style.border = "3px solid red";
		buttonRegister.disabled = true;
	} else {
		password.style.border = "3px solid green";
		repeatPassword.style.border = "3px solid green";
		buttonRegister.disabled = false;
	}
	
	if (password.value === "") {
		password.style.border = "none";
	}
	
	if (repeatPassword.value === "") {
		repeatPassword.style.border = "none";
	}
}
*/
function validateSignUp() {
	//Email
	var email = document.getElementById("email");
	var showValidEmail = document.getElementById("showValidEmail");
	var showInvalidEmail = document.getElementById("showInvalidEmail");

	//Username
	var username = document.getElementById("username");
	var showValidUsername = document.getElementById("showValidUsername");
	var showInvalidUsername = document.getElementById("showInvalidUsername");

	//Password
	var password = document.getElementById("password");
	var showValidPassword = document.getElementById("showValidPassword");
	var showInvalidPassword = document.getElementById("showInvalidPassword");

	//Repeat password
	var repeatPassword = document.getElementById("repeatPassword");
	var showValidRepeatPassword = document.getElementById("showValidRepeatPassword");
	var showInvalidRepeatPassword = document.getElementById("showInvalidRepeatPassword");

	//Button register
	var buttonRegister = document.getElementById("buttonSubmit");

	//Regular expressions
	var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var usernamePattern = /^[a-z0-9]{6,}$/;
    var passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	
	// Check inputs if regexp match
	var isEmailValid = emailPattern.test(email.value);
    var isUsernameValid = usernamePattern.test(username.value);
    var isPasswordValid = passwordPattern.test(password.value);
	var isRepeatPasswordValid = passwordPattern.test(repeatPassword.value);
    var arePasswordsMatching = (password.value === repeatPassword.value);
	
	// Email
	if (!isEmailValid) {
      email.style.border = "solid 3px red";
	  showInvalidEmail.style.display = "block";
	  showValidEmail.style.display = "none";
    } else {
      email.style.border = "solid 3px green";
	  showInvalidEmail.style.display = "none";
	  showValidEmail.style.display = "block";
    }
	
	
	// Username
	if (!isUsernameValid) {
		username.style.border = "solid 3px red";
		showInvalidUsername.style.display = "block";
		showValidUsername.style.display = "none";
    } else {
		username.style.border = "solid 3px green";
		showInvalidUsername.style.display = "none";
		showValidUsername.style.display = "block";
    }
	
	// Password
	if (!isPasswordValid) {
		password.style.border = "solid 3px red";
		showInvalidPassword.style.display = "block";
		showValidPassword.style.display = "none";

	} else {
		password.style.border = "solid 3px green";
		showInvalidPassword.style.display = "none";
		showValidPassword.style.display = "block";
	}

	// Repeat password
	if (!isRepeatPasswordValid || !arePasswordsMatching) {

		repeatPassword.style.border = "solid 3px red";
		showInvalidRepeatPassword.style.display = "block";
		showValidRepeatPassword.style.display = "none";

	} else if (repeatPassword.value == "") {
		repeatPassword.style.border = "solid 3px red";
		showInvalidRepeatPassword.style.display = "block";
		showValidRepeatPassword.style.display = "none";
	} else {
		repeatPassword.style.border = "solid 3px green";
		showInvalidRepeatPassword.style.display = "none";
		showValidRepeatPassword.style.display = "block";
	}
	
	// Validation of all
	if (isEmailValid && isUsernameValid && isPasswordValid && isRepeatPasswordValid && arePasswordsMatching) {
		buttonRegister.disabled = false;
    } else {
      	buttonRegister.disabled = true;
    }
}

/* function validatePassword(password) {
	// var password1 = document.getElementById("password");
	var password1 = password
	
	var passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	var isPasswordValid = passwordPattern.test(password1.value.replace(/\s/g, ""));

	
	// Password
	if (!isPasswordValid) {
		password1.style.border = "3px solid red";
	} else {
		password1.style.border = "3px solid green";
	}
		
}
function validateRepeatPassword(repeatpassword) {
	var password1 = document.getElementById("password");
	var repeatPassword = repeatpassword;
	var buttonRegister = document.getElementById("buttonSubmit");
	
    var arePasswordsMatching = (password1.value.replace(/\s/g, "") === repeatPassword.value.replace(/\s/g, ""));
	
	if (!arePasswordsMatching) {
		repeatPassword.style.border = "3px solid red";
		repeatPassword.style.backgroundImage  = "none !important";
	} else {
		repeatPassword.style.border = "3px solid green";
	}
	
	if (!arePasswordsMatching){
		buttonRegister.disabled = true;
	} else {
		buttonRegister.disabled = false;
	}
		
}
 */
function validatePasswordProfile() {
	// Current password
	var currentPassword = document.getElementById("current_password");
	var showInvalidCurrentPassword = document.getElementById("showInvalidCurrentPassword");

	// New password
	var newPassword = document.getElementById("password");
	var showInvalidNewPassword = document.getElementById("showInvalidNewPassword");

	// Repeat new password
	var repeatPassword = document.getElementById("repeatPassword");
	var showInvalidRepeatNewPassword = document.getElementById("showInvalidRepeatPassword");
	
	//Button register
	var buttonSubmit = document.getElementById("buttonSubmit");

	// Regular expression
	var passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;

	// Check input if regexp match
	var isCurentPasswordValid = passwordPattern.test(currentPassword.value);
    var isNewPasswordValid = passwordPattern.test(newPassword.value);
	var isRepeatPasswordValid = passwordPattern.test(repeatPassword.value);
    var arePasswordsMatching = (newPassword.value === repeatPassword.value);

	// Current password
	if (!isCurentPasswordValid) {
		currentPassword.style.border = "solid 3px red";
		showInvalidCurrentPassword.style.display = "block";
	} else {
		currentPassword.style.border = "solid 3px green";
		showInvalidCurrentPassword.style.display = "none";
	}

	// New password
	if (!isNewPasswordValid) {
		newPassword.style.border = "solid 3px red";
		showInvalidNewPassword.style.display = "block";
	} else {
		newPassword.style.border = "solid 3px green";
		showInvalidNewPassword.style.display = "none";
	}

	// Repeat password
	if (!isRepeatPasswordValid || !arePasswordsMatching) {

		repeatPassword.style.border = "solid 3px red";
		showInvalidRepeatNewPassword.style.display = "block";

	} else if (repeatPassword.value == "") {
		repeatPassword.style.border = "solid 3px red";
		showInvalidRepeatNewPassword.style.display = "block";
	} else {
		repeatPassword.style.border = "solid 3px green";
		showInvalidRepeatNewPassword.style.display = "none";
	}

	// Validation of all
	if (isCurentPasswordValid && isNewPasswordValid && isRepeatPasswordValid && arePasswordsMatching) {
		buttonSubmit.disabled = false;
	} else {
		buttonSubmit.disabled = true;
	}
	
}

function checkPassword() {
	var password = document.getElementById("password");
	var repeatPassword = document.getElementById("repeatPassword");

	if (password.type === "password" && repeatPassword.type === "password") {
		password.type = "text";
		repeatPassword.type = "text";
	} else {
		password.type = "password";
		repeatPassword.type = "password";
  	}
}

function checkCurrentPassword() {
	var current_password = document.getElementById("current_password");

	if (current_password.type === "password") {
		current_password.type = "text";
	} else {
		current_password.type = "password";
  	}
}