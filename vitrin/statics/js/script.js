let body = document.getElementsByTagName('body');
let btn = document.querySelector('button');


let new_div = document.createElement('div');
let new_h3 = document.createElement('h3');
new_div.appendChild(new_h3);
new_div.style.border = 'solid black 2px';
new_div.style.margin = 'auto';
new_div.style.marginTop = '10px';
new_div.style.width = '40%';


// ********** Test sending AJAX request to the server **************
btn.addEventListener('click', e => {
    fetch('http://127.0.0.1:8000/ajax-response-test')
    .then(response => {
        // console.log(response)
        console.log('All "response" headers (include "NAME" custom header) listed below:');
        if (!response.ok){
            return Promise.reject('AJAX Error: No resource found!')
        }
        response.headers.forEach((h, k) => {
        console.log(k, ' ==> ', h);
        })
        console.log('');
        return response.json();
    })
    .then(json => {
        // console.log(json);
        if(json.status === 'ok'){
            new_div.style.borderColor = 'green';
            new_h3.style.color = 'blue';
        }
        else{
            new_div.style.borderColor = 'red';
            new_h3.style.color = 'orange';
        }
        new_h3.innerText = json.msg;
        // new_h3.innerText = JSON.stringify(json);
        body[0].appendChild(new_div);
    })
    .catch(err => {
        console.log(err);
    })
})