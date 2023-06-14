let form = document.querySelector('#contact-us-form');


// Form validation for contact-us
form.addEventListener('submit', e=>{
    e.preventDefault();
    let errors = 0;
    let name = form['name'].value;
    let subject = form['subject'].value;
    let message = form['message'].value;
    let subjectError = document.querySelector('.subject-error');
    let messageError = document.querySelector('.message-error');
    subjectError.innerHTML = '';
    messageError.innerHTML = '';
    form['subject'].style.borderColor = '#dee2e6';
    form['message'].style.borderColor = '#dee2e6';
    if(subject.length < 1){
        subjectError.innerHTML = 'لطفا موضوع پیام خود را وارد کنید';
        form['subject'].style.borderColor = 'red';
        errors += 1;
    }
    if(message.length < 1){
        messageError.innerHTML = 'پیام خود را وارد کنید';
        form['message'].style.borderColor = 'red';
        errors += 1;
    }
    if(!errors){
        form.submit();
    }
})