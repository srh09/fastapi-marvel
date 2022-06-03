const BASE_URI = 'http://127.0.0.1:8000';
const EMPTY_CHARACTER = {
    'marvel_id': '12345',
    'name': null,
    'description': null,
    'thumbnail': Error.src,  // Hackz
};

const asyncTimeout = delay => new Promise(resolve => setTimeout(resolve, delay));
const sendAsyncRequest = async (method, endpoint, payload) => {
    const uri = `${BASE_URI}${endpoint}`;
    const requestOptions = {
        method: method,
        headers: { 'Content-Type': 'application/json', 'charset': 'utf-8'},
    };
    if (payload) requestOptions['body'] = JSON.stringify(payload);
    const response = await fetch(uri, requestOptions);
    if (!response.ok) {
        throw `HTTP Exception Status:${response.status}`
    };
    return await response.json();
}

const marvel = () => {
    return {
        loading: false,
        characterSearch: '',
        character: EMPTY_CHARACTER,
        async clearCharacter() {
            this.loading = true;
            await asyncTimeout(250);
            this.characterSearch = ''
            this.character = EMPTY_CHARACTER
            this.loading = false;
        },
        async getByNameCharacter() {
            // Dont send on empty.
            if (!this.characterSearch) return

            // Fade out elements.
            this.loading = true;

            // Timeout for animation.
            await asyncTimeout(250);

            // Get the data.
            let response = null;
            try {
                response = await sendAsyncRequest('GET', `/api/v1/character?name=${this.characterSearch}`);
            } catch (error) {
                // TODO: Some kind of 'character not found' banner on 404?
                response = EMPTY_CHARACTER;
            }

            // Bind the data.
            this.character = (response && Object.keys(response).length) ? response : EMPTY_CHARACTER;
            
            // Timeout for image load.
            await asyncTimeout(1000);

            // Fade in elements.
            this.loading = false;
        }
    }
}

const sayHi = () => console.log('Hi there------')
const sayBye = () => console.log('goodbye-----')

const logo = document.getElementById('logo-svg');
logo.addEventListener('mouseenter', () => {
    logo.style.animation = "runAway 8s"
});
logo.addEventListener('animationend', () => {
    logo.style.animation = null;
});
