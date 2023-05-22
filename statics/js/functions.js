// * Used to check if input is a valid email
const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };


// * Validate mobile phone
const check_phone = (number) => {
    var regex = new RegExp("^(\\+98|0)?9\\d{9}$");
    var result = regex.test(number);
    return result;
};


// Helper to add 1 to the product--cart input number
let addOne = (inputNode, max=5) => {
    if(Number(inputNode.value < max)){
        inputNode.value = Number(inputNode.value) + 1;
    }
}
// Helper to minus 1 to the product input number
let minuseOne = (inputNode, min=1) => {
    if(Number(inputNode.value > min)){
        inputNode.value = Number(inputNode.value) - 1;
    }
}


// Change product quantity
let checkCartQuantity = (nodeValue=new Node, emptyCartElem=new Node, fullCartElem) => {
    let value = Number(nodeValue.innerText);
    if(value > 0){
        emptyCartElem.classList.add('d-none');
    }
    else{
        fullCartElem.remove();
        emptyCartElem.classList.remove('d-none');
    }
}


// For forms, check if 'accept rules button' is checked by user
const checkRulesBorder = (checkoutElem, buttonElem) => {
    if(!checkoutElem.checked && buttonElem.disabled){
        checkoutElem.style.borderColor = 'red';
        return false;
    }
    else{
        checkoutElem.style.borderColor = '#dee2e6';
        return true;
    }
}


// In forms, if user does no check the 'accept rules', the submit button disabled
const disabledSubmitRule = (buttonElem, e) => {
    if(e.target.checked){
        buttonElem.disabled = false;
    }
    else{
        buttonElem.disabled = true;
    }
}


// Validate user sing up data
const signUpDataValidation = (username=new String, password=new String, confrimPassword=new String) => {
    const usernameError = document.querySelector('.signup-username-error');
    const passwordError = document.querySelector('.signup-password-error');
    const confirmPasswordError = document.querySelector('.signup-password-cofirm-error');
    usernameError.innerText = '';
    passwordError.innerText = '';
    confirmPasswordError.innerText = '';
    let errors = 0;
    // Username validation
    if(username.length < 1){
        usernameError.innerText = 'ایمیل یا شماره تماس  خود را وارد کنید';
        errors += 1;
    }
    if(!(validateEmail(username) || check_phone(username))){
        usernameError.innerText = 'ایمیل یا شماره تماس خود را به درستی وارد کنید';
        errors += 1;
    }
    // Password validation
    if(password.length == 0){
        passwordError.innerText = 'رمز عبور را وارد کنید';
        errors += 1;
    }
    if(1 <= password.length && password.length <= 4){
        passwordError.innerText = 'طول رمز عبور باید بیش از 4 کاراکتر باشد';
        errors += 1;
    }
    if(password.length >= 15){
        passwordError.innerText = 'طول رمز عبور باید کمتر از 15 کاراکتر باشد';
        errors += 1;
    }
    // ConfirmPassword validation
    if(confrimPassword.length == 0){
        confirmPasswordError.innerText = 'تکرار رمز عبور را وارد کنید';
        errors += 1;
    }
    if(password != confrimPassword){
        confirmPasswordError.innerText = 'تکرار رمز عبور اشتباه است';
        errors += 1;
    }
    if(errors == 0){
        usernameError.innerText = '';
        passwordError.innerText = '';
        confirmPasswordError.innerText = '';
        return true;
    }
    return false;
}


// Sign in data validation
const signInDataValidation = (username, password) => {
    const usernameError = document.querySelector('.signin-username-error');
    const passwordError = document.querySelector('.signin-password-error');
    usernameError.innerText = '';
    passwordError.innerText = '';
    let errors = 0;
    // Username validation
    if(username.length < 1 || !validateEmail(username) || check_phone(username)){
        if(username.length < 1){
            usernameError.innerText = 'ایمیل یا شماره همراه خود را وارد کنید';
            errors += 1;
        }
        else if(!(validateEmail(username) || check_phone(username))){
            usernameError.innerText = 'ایمیل یا شماره همراه خود را به درستی وارد کنید';
            errors += 1;
        }
    }
    // Password validation
    if(password.length == 0){
        passwordError.innerText = 'رمز عبور را وارد کنید';
        errors += 1;
    }
    if(errors == 0){
        usernameError.innerText = '';
        passwordError.innerText = '';
        return true;
    }
    return false;
}


export {validateEmail, check_phone, addOne, minuseOne, 
    checkCartQuantity, checkRulesBorder, disabledSubmitRule,
    signUpDataValidation, signInDataValidation};