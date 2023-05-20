import {sendPostData} from './ajax.js';
import {validateEmail} from './functions.js';
import getCookie from './csrftoken.js';



// *** Activate related profile content section for clicked icon ***
const iconList = document.querySelector('.profile-icons-list');

iconList.addEventListener('click', e => {
    e.preventDefault();
    const icons = document.querySelectorAll('.profile-icons-list > i');
    const profileContentSections = document.querySelectorAll('.profile-content > div');
    
    if(e.target.tagName == 'I' && !e.target.classList.contains('active')){
        // Disable display of current profile content section
        Array.from(icons).forEach(iconNode => {
            profileContentSections.forEach(profileContentNode => {
                profileContentNode.classList.remove('active');
                // Display related contents based on selected icon (Actually this is could be the last step but this way is more optimal)
                if(profileContentNode.getAttribute('data-icon-content') == e.target.getAttribute('data-icon-content')){
                    profileContentNode.classList.add('active');
                }
            })
            // Disable current selected icon from icon list
            iconNode.classList.remove('active');
        })
        // Enlarge clicked icon from icon list
        e.target.classList.add('active');
    }
})



// *** Change password from Profile Security section (panel) ***
let changePasswordForm = document.querySelector('#profile-password-change-form');
let changePasswordResult = document.querySelector('.profile-security-result');

changePasswordForm.addEventListener('submit', e => {
    e.preventDefault();
    let formData = new FormData(changePasswordForm);
    const currentPassword = formData.get('password-current');
    const newPassword = formData.get('password-new');
    const confirmPassword = formData.get('password-new-confirm');
    changePasswordResult.innerText = '';
    
    // * Data validation of password form
    const passwordChangeDataValidation = () => {
        const currentPasswordError = document.querySelector('.profile-security-current-password');
        const newPasswordError = document.querySelector('.profile-security-new-password');
        const confirmPasswordError = document.querySelector('.profile-security-confirm-password');
        currentPasswordError.innerText = '';
        newPasswordError.innerText = '';
        confirmPasswordError.innerText = '';
        let errors = 0;

        // Current password validation
        if(currentPassword.length == 0){
            currentPasswordError.innerText = 'رمز عبور را وارد کنید';
            errors += 1;
        }

        // New password validation
        if(newPassword.length == 0){
            newPasswordError.innerText = 'رمز عبور جدید را وارد کنید';
            errors += 1;
        }
        if(1 <= newPassword.length && newPassword.length <= 4){
            newPasswordError.innerText = 'طول رمز عبور باید بیش از 4 کاراکتر باشد';
            errors += 1;
        }
        if(newPassword.length >= 15){
            newPasswordError.innerText = 'طول رمز عبور باید کمتر از 15 کاراکتر باشد';
            errors += 1;
        }
        // ConfirmPassword validation
        if(confirmPassword.length == 0){
            confirmPasswordError.innerText = 'تکرار رمز عبور را وارد کنید';
            errors += 1;
        }
        if(newPassword != confirmPassword){
            confirmPasswordError.innerText = 'تکرار رمز عبور اشتباه است';
            errors += 1;
        }
        // Compare current and new passwords
        if(currentPassword.length > 0 && newPassword.length > 0 && currentPassword === newPassword){
            currentPasswordError.innerText = 'رمز عبور جدید و قدیم نمیتواند یکسان باشند';
            errors += 1;
        }
        if(errors == 0){
            currentPasswordError.innerText = '';
            newPasswordError.innerText = '';
            confirmPasswordError.innerText = '';
            return true;
        }
        else{
            return false;
        }
    }

    // * Send data to server
    if(passwordChangeDataValidation()){
        const url = 'http://127.0.0.1:8000/password-change';
        const data = {password: currentPassword, 'new-password': newPassword};
        const error = 'پیام ارسال نشد';
        sendPostData(url, data, error)
        .then(data => {
            console.log(data);
            if(data.status == 200){
                changePasswordResult.innerText = 'تغییر رمز با موفقیت انجام شد';
                changePasswordResult.style.color = 'green';
            }
            else{
                changePasswordResult.innerText = 'تغییر رمز انجام نشد';
                changePasswordResult.style.color = 'red';
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
})



// *** Edit profile ***
let editProfilePanel = document.querySelector('.profile-edit');
let editSubmitButton = document.querySelector('#profile-edit-submit');
let profileEditForm = document.querySelector('#profile-edit-form');
const editProfileInputs = document.querySelectorAll('.edit-profile-form-input');

// * enable-disable input box for each input by click on its pen icon (except for profile image)
editProfilePanel.addEventListener('click', e => {
    if(e.target.classList.contains('edit-icon')){
        const editIcon = e.target;
        let editInput = null;
        Array.from(editIcon.parentElement.children).forEach(elem => {
            if(elem.tagName === 'INPUT'){
                editInput = elem;
            }
        })
        if(editInput){
            if(editInput.disabled){
                editInput.disabled = false;
            }
            else{
                editInput.disabled = true;
            }
        }
    }
})

// * If each input changes, submit button should be enabled
let changedData = new Object();

Array.from(editProfileInputs).forEach(editInput => {
    let oldInputValue = editInput.value;
    editInput.addEventListener('input', e => {
        let newInputValue = editInput.value;
        let fieldName = editInput.getAttribute('name');
        if(oldInputValue !== newInputValue){
            editSubmitButton.disabled = false;
            changedData[fieldName] = newInputValue;
        }
        else{
            delete changedData[fieldName];
        }
    })
})

// * Submit form and validate data
let emailError = document.querySelector('.email-error');
let phoneError = document.querySelector('.phone-error');
let firstNameError = document.querySelector('.first-name-error');
let lastNameError = document.querySelector('.last-name-error');
let addressError = document.querySelector('.address-error')
const editProfileResult = document.querySelector('.edit-profile-result');

profileEditForm.addEventListener('submit', e => {
    e.preventDefault();
    emailError.innerText = '';
    phoneError.innerText = '';
    firstNameError.innerText = '';
    lastNameError.innerText = '';
    addressError.innerText = '';
    editProfileResult.innerText = '';
    let errors = 0;
    // Validate data
    Object.keys(changedData).forEach(key => {
        if(key == 'email'){
            if(changedData[key].length == 0){
                emailError.innerText = 'ایمیل را وارد کنید';
                errors += 1;
            }
            if(!validateEmail(changedData[key])){
                emailError.innerText = 'ایمیل خود را به درستی وارد کنید';
                errors += 1;
            }
        }
    }) 
    if(errors >= 1){
        console.log('there are lot of errors');
    }
    // If there is no error in validation, send data to server
    else{
        let url = 'http://127.0.0.1:8000/edit-profile';
        let errMsg = 'داده ها به خوبی ارسال نشد';
        sendPostData(url, changedData, errMsg)
        .then(data => {
            console.log(data);
            if(data.status == 200){
                editProfileResult.style.color = 'green';
                editProfileResult.innerText = 'پروفایل با موفقیت آپدیت شد';
            }
            else{
                editProfileResult.style.color = 'red';
                editProfileResult.innerText = 'پروفایل آپدیت نشد';
            }
            editSubmitButton.disabled = true;
        })
        .catch(err => {
            console.log(err);
        })
    }
})

// * Upload-change user image
let profileImageInput = document.querySelector('#upload-profile-image');
const profileImageVerifyButton = document.querySelector('#verify-new-image');
let profileCurrentImage = document.querySelector('#profile-edit-current-image');
let profileNewImage = document.querySelector('.profile-edit-uploaded-image');
var image = null;

// Upload and show image to user before submit the image
profileImageInput.addEventListener('change', e => {
    image = document.createElement('img');
    image.src = profileImageInput.files[0].name;
    image.width = '150';
    image.height = '150';
    // image.style.borderRadius = '50%';
    profileNewImage.appendChild(image);
    profileImageVerifyButton.classList.remove('d-none');
})

// Submit the image verify button
profileImageVerifyButton.addEventListener('click', e => {
    e.preventDefault();
    let url = 'http://127.0.0.1:8000/edit-profile-image'
    // Because the data is a file (not jsonizable) we cannot use 'sendPostData'
    let data = new FormData();
    data.append('image', profileImageInput.files[0]);
    const csrftoken = getCookie('csrftoken');
    fetch(url, {
        method: 'POST',
        body: data,
        credentials: 'include',
        mode: 'cors',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if(response.status != 200 || !response.ok){
            return Promise.reject('مشکلی پیش آمده');
        }
        return response.json();
    })
    .then(data => {
        // If server responds with success, replace current image with new image
        console.log(data);
        if(data.status == 200){
            profileCurrentImage.src = profileImageInput.files[0].name;
            image.remove();
            profileImageVerifyButton.classList.add('d-none');
        }
    })
    .catch(err => {
        console.log(err);
    })
})