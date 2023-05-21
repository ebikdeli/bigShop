import {checkRulesBorder, disabledSubmitRule, signUpDataValidation} from '../functions.js';
import { sendPostData } from '../ajax.js';


let acceptButton = document.querySelector('input[type="checkbox"]');
let submitButton = document.querySelector('#submit-button');


// * Check rules box
submitButton.parentElement.addEventListener('click', e => {
    e.preventDefault();
    const ruleChecked = checkRulesBorder(acceptButton, submitButton);
    // * If rule checkbox is checked, validate form data
    if(ruleChecked){
        const username = document.querySelector('[name="username"]').value;
        const password = document.querySelector('[name="password"]').value;
        const passwordConfirm = document.querySelector('[name="password_confirm"]').value;
        // If data validation was successful, send data to server
        if(signUpDataValidation(username, password, passwordConfirm)){
            const url = 'http://127.0.0.1:8000/login/signup/';
            const data = {username: username, password: password};
            const err = 'مشکلی در اتصال پیش آمده';
            sendPostData(url, data, err)
            .then(data => {
                console.log(data);
                console.log(data.status);
                if(data.status === 300){
                    alert('This user already exists')
                }
                if(data.status === 201){
                    console.log(data.msg);
                    window.location.replace('http://127.0.0.1:8000/')
                }
            })
            .catch(err => {
                console.log(err);
            })
        }
    }
})

acceptButton.addEventListener('change', e => {
    e.preventDefault();
    disabledSubmitRule(submitButton, e);
})


// NOTE: Because we already added an eventListener for the 'submit' button, 'submit' evenrlistener
// does not work for the form. So we process form data in the 'click' eventListener of the submit button
// signUpForm.addEventListener('submit', e => {
//     e.preventDefault();
//     // ...
// })