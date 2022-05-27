const BASE_URI = 'http://127.0.0.1:8000'

async function sendAsyncRequest(method, endpoint, payload) {
    const uri = `${BASE_URI}${endpoint}`;
    const requestOptions = {
        method: method,
        headers: { 'Content-Type': 'application/json', 'charset': 'utf-8'},
    }
    if (payload) requestOptions['body'] = JSON.stringify(payload);
    const response = await fetch(uri, requestOptions);
    if (!response.ok) {
        console.log('there was an error------')
        return;
    }
    return await response.json();
}

const marvel = () => {
    return {
        characterSearch: '',
        character: {},
        async getTestPage() {
            console.log('getting the test page----')
        },
        async getCharacter() {
            console.log('I am about to get a character----')
            response = await sendAsyncRequest('GET', '/api/v1/character?name=spectrum')
            console.log('i got a character-----')
            console.log(response)
            this.character = response
        }
    }
}

const sayHi = () => console.log('Hi there------')
const sayBye = () => console.log('goodbye-----')

const logo = document.getElementById('logo-svg')
logo.addEventListener('mouseenter', () => {
    logo.style.animation = "runAway 8s"
})
logo.addEventListener('animationend', () => {
    logo.style.animation = null;
})
