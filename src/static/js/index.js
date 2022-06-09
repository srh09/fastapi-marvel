const BASE_URI = 'http://127.0.0.1:8000';
const EMPTY_CHARACTER = {
    'marvelId': '12345',
    'name': null,
    'description': null,
    'comics': 'Comics: ',
    'series': 'Series: ',
    'stories': 'Stories: ',
    'thumbnail': ' ',
};

const EMPTY_COMIC = {
    'title': 'The Mighty Captain Marvel Vol. 2: Band of Sisters (Trade Paperback) asdasdasdasdasd',
    'issueNumber': 'Issue Number: 0',
    'pageCount': 'Page Count: 112',
    'isbn': 'ISBN: 978-1-302-90606-1',
    'description': "Collects The Mighty Captain Marvel (2016) #5-9. As SECRET EMPIRE begins, Captain Marvel faces the Chitauri! The savage alien fleet has nearly reached Earth space, and it’s up to Carol Danvers to stop it. But taking on an entire armada is a tall order even for our mighty hero and the crew of the Alpha Flight Space Station.",
    'thumbnail': "http://i.annihil.us/u/prod/marvel/i/mg/9/70/5a32a9ef950c5.jpg",
    'urlDetail': 'http://marvel.com/comics/collection/62125/the_mighty_captain_marvel_vol_2_band_of_sisters_trade_paperback?utm_campaign=apiRef&utm_source=08763b6aa625b3ecce0c74e79d3e4273'
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
        hasCharacter: false,
        hasComic: false,
        hasComics: false,
        hasAffiliate: false,
        character: EMPTY_CHARACTER,
        comic: EMPTY_COMIC,
        comics: [EMPTY_COMIC, EMPTY_COMIC],
        async clearCharacter() {
            this.hasCharacter = false;
            this.characterSearch = ''
            await asyncTimeout(250);
            this.character = EMPTY_CHARACTER
        },
        async getCharacterByName() {
            // Dont send on empty.
            if (!this.characterSearch) return;

            // Fade out elements.
            this.hasCharacter = false;

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
            this.hasCharacter = true;
        },
        async getComicsByCharacter() {
            console.log('get comics by character------')
            response = await sendAsyncRequest('GET', `/api/v1/comics/character/${this.character.marvelId}`)
            this.comics = Object.values(response)
        },
        getComicDetail(comic) {
            console.log('get comic detail---------')
            console.log(comic)
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
