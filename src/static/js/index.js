const BASE_URI = 'http://127.0.0.1:8000';
const EMPTY_CHARACTER = {
    'hasData': false,
    'marvelId': '12345',
    'name': null,
    'description': null,
    'comics': 'Comics: ',
    'series': 'Series: ',
    'stories': 'Stories: ',
    'thumbnail': ' ',
};

const EMPTY_COMICS = {
    'hasData': false,

}

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
        characterSearch: '',
        character: EMPTY_CHARACTER,
        async clearCharacter() {
            this.character.hasData = false;
            this.characterSearch = ''
            await asyncTimeout(250);
            this.character = EMPTY_CHARACTER
        },
        async getCharacterByName() {
            // Dont send on empty.
            if (!this.characterSearch) return;

            // Fade out elements.
            this.character.hasData = false;

            // Timeout for animation.
            await asyncTimeout(250);

            // Get the data.
            let response = null;
            try {
                response = await sendAsyncRequest('GET', `/api/v1/character?name=${this.characterSearch}`);
            } catch (error) {
                // TODO: Some kind of 'character not found' banner on 404?
                return;
            }

            // Bind the data.
            // this.character = (response && Object.keys(response).length) ? response : EMPTY_CHARACTER;
            this.character = {
                'marvelId': response['marvel_id'],
                'name': response['name'],
                'description': response['description'],
                'comics': `Comics: ${response['comic_count']}`,
                'series': `Series: ${response['series_count']}`,
                'stories': `Stories: ${response['stories_count']}`,
                'thumbnail': response['thumbnail'],
            }

            // Timeout for image load.
            await asyncTimeout(1000);
            console.log('here----')
            // Fade in elements.
            this.character.hasData = true;
        },
        async getComicsByCharacter() {
            console.log('get comics by character------')
            // response = await sendAsyncRequest('GET', `/api/v1/comics/character/${this.character.marvelId}`)
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
