import { signInDataValidation } from "../functions.js";
import { sendPostData } from '../ajax.js';


const signInForm = document.forms['login--form'];
const usernameError = document.querySelector('.signin-username-error');

signInForm.addEventListener('submit', e => {
    e.preventDefault();
    let username = document.querySelector('input[name="username"]').value;
    let password = document.querySelector('input[name="password"]').value;
    if(signInDataValidation(username, password)){
        let url = 'http://127.0.0.1:8000/login/login/';
        let data = {username: username, password: password};
        let err = 'خطا در برقراری ارتباط با سرور';
        sendPostData(url, data, err)
        .then(data => {
            console.log(data);
            if(data.status === 200){
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'با موفقیت وارد شدید',
                    showConfirmButton: false,
                    timer: 2000
                  })
                window.location.replace('http://127.0.0.1:8000/dashboard')
            }
            else{
                Swal.fire(
                    'ورود انجام نگرفت',
                    'نام کاربری یا رمز عبور اشتباه است',
                    'warning'
                  )
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
})