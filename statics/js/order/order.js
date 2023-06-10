import { validateEmail, check_phone } from "../functions.js";


// * Validate order-form inputs
let orderForm = document.querySelector('#order-form');
let orderFormError = document.querySelector('.order-form-error');


orderForm.addEventListener('submit', e=>{
    e.preventDefault();
    orderFormError.innerHTML = '';
    let errors = 0;
    let email = e.target['email'];
    let phone = e.target['phone'];
    let postal = e.target['postal'];

    Array.from(document.querySelectorAll('#order-form .form-control')).forEach(elem=>{
        // Check if there is empty inputs in the form
        if(!elem.value){
            elem.style.borderColor = 'red';
            errors += 1;
        }
        else{
            elem.style.borderColor = 'grey';
        }
    })
    // email validation
    if(email.value.length > 1 && !validateEmail(email.value)){
        email.style.borderColor = 'red';
        orderFormError.innerHTML += '<small>ایمیل خود را به درستی وارد کنید</small>';
        errors += 1;
    }
    // phone validation
    if(phone.value.length > 1 && !check_phone(phone.value)){
        phone.style.borderColor = 'red';
        orderFormError.innerHTML += '<small>شماره تماس خود را به درستی وارد کنید</small>';
        errors += 1;
    }
    // Check if postal is only number with 10 character length
    if (!(postal.value.length === 10 && (/^\d+$/.test(postal.value)))) {
        postal.style.borderColor = 'red';
        orderFormError.innerHTML += '<small>کد پستی را به درستی وارد کنید</small>';
        errors += 1;
    }
    // If there is no error in validating the form, submit the form
    if(errors < 1){
        orderForm.submit();
    }
})