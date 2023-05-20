import getCookie from './csrftoken.js';


// Ajax POST request to server
const sendPostData = async (url=new String, data=new Object, errMsg=new String) => {
    try{
        const csrftoken = getCookie('csrftoken');
        let jsonData = data;
        if(!(data instanceof FormData)){
            jsonData = new FormData();
            jsonData.append('data', JSON.stringify(data));
        }
        const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            mode: 'cors',
            body: jsonData,
            headers: {
                'X-CSRFToken': csrftoken,
            }
        })
        if(response.status !== 200 || !response.ok){
            return Promise.reject(errMsg);
        }
        let jsonResponse = await response.json();
        return jsonResponse;
    }
    catch(err){
        console.log(err);
        if(err instanceof TypeError){
            return Promise.reject('اتصال با سرور برقرار نشد');
        }
    }
}


export {sendPostData};