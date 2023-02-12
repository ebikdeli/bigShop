// When using Event Listeners, remember to first thing to do is to call preventDefault() for the eventObject
// NOTE: With 'windows.location' we can get current site url, host, server and even redirect user to another url:
// EG: redirect user to another url:   location.replace('http://127.0.0.1:8000/');
// NOTE *: When using 'FormData' in 'POST' request, we should set 'Content-Type' header and let the 'fetch' decide what it should be because we received an error that documented in the followin address:
// https://stackoverflow.com/questions/39280438/fetch-missing-boundary-in-multipart-form-data-post
// NOTE: Question: How to know if a request, is Ajax call or a simple web request by the browser?
// Answer: Most of Ajax technologies (Fetch for example) as for 'HTTP_ACCEPT' header, uses '*/*' by default. If we set request header 'Accept: application/json' for example,
// ... then at server we receive 'HTTP_ACCEPT = 'pplication/json'. This way we know the request is Ajax call. But in ordinary web request by browser, value of 'HTTP_ACCEPT' is something like this in below:
// ... text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
// https://stackoverflow.com/questions/8508602/check-if-request-is-ajax-in-python

let body = document.getElementsByTagName('body');
let btn = document.querySelector('button');
let form = document.querySelector('form');
// **** Remember to get form data with 'FormData' object after submitting the form not before it!
// console.log(document.forms['form']);

form.addEventListener('submit', e => {
    let is_validated = prompt('Is form validated?\nPress "y" as yes and "n" as no\nAnything else let the django fullstack handles the form');
    console.log('Form should validated');
    if(is_validated === 'n'){
        console.log('Form not validated!');
        e.preventDefault();
    }
    else{
        location.reload();
    }
})

// ** Define new div with needed style to process further server response from Ajax request
let new_div = document.createElement('div');
let new_h3 = document.createElement('h3');
new_div.appendChild(new_h3);
new_div.style.border = 'solid black 2px';
new_div.style.margin = 'auto';
new_div.style.marginTop = '10px';
new_div.style.width = '40%';

// ********** Test sending AJAX request to the server **************
btn.addEventListener('click', e => {
    e.preventDefault();
    // * Submit the form first
    let form_data = new FormData(form);
    form_data.append('name', 'ehsan');
    form_data.append('password', '123456');
    for(let entry of form_data){
        console.log(entry);
    }

    // * Get csrftoken to send to server for POST request
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // * Send Ajax request to the server
    // NOTE: following command used to demonstrate how we can send data to server using parameters in url when using 'GET' method.
    let dt = `name=ehsan&csrftoken=${csrfToken}`;
    // NOTE: To send 'data' with 'POST' method, value of 'Content-Type' header is only limited to the three choices that 'enctype' attribute of <form> tag accepts
    fetch(`http://127.0.0.1:8000/ajax-response-test?${dt}`,
    {
        method: 'POST',
        // method: 'GET',
        body: form_data,
        // body: JSON.stringify({name:'ehsan', age: 30}),
        mode: 'same-origin',
        headers: {
            // 'Content-Type': 'application/json',     // Default value of the 'Content-Type' is 'text/plain'
            // 'Content-Type': 'application/x-www-form-urlencoded',     // When using FormData in "POST" request, we should not set 'Content-Type' because WebKitBoundaries will fail!!! and we must let the JS set that by default!
            'X-CSRFToken': csrfToken,
            // 'Accept': 'application/json'     It is very useful to inform the server what type of Response, the client expects to receive. specially when there are diffrent types of calls available like Ajax call, browser call and mobile device call
        },
    })
    .then(response => {
        // console.log(response)
        console.log('All "response" headers (include "NAME" custom header) listed below:');
        if (response.status == 404){
            return Promise.reject('AJAX Error: No resource found!');
        }
        else if(response.status == 403){
            return Promise.reject('Unauthorized request to server!');
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