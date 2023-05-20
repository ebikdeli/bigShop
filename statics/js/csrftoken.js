// * Function to get any cookie we want based on this resource:
// https://docs.djangoproject.com/en/dev/howto/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// * When define a script as a module, we should use 'export' to identify the code we want to import in other scripts. And every module should have a code as 'default'!
export {getCookie as default};