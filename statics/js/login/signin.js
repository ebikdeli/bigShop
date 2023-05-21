import { signInDataValidation } from "./functions.js";
import { sendPostData } from '../ajax.js';


const signInForm = document.forms['login--form'];
const emailError = document.querySelector('.signin-email-error');

signInForm.addEventListener('submit', e => {
    e.preventDefault();
    let username = document.querySelector('input[name="username"]').value;
    let password = document.querySelector('input[name="password"]').value;
    if(signInDataValidation(email, password)){
        let url = 'http://127.0.0.1:8000/login/signin';
        let data = {username: username, password: password};
        let err = 'خطا در برقراری ارتباط با سرور';
        sendPostData(url, data, err)
        .then(data => {
            console.log(data);
            if(data.status !== 200){
                emailError.innerText = 'این ایمیل ثبت نام نشده';
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
})