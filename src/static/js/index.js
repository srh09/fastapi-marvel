const FADE_TIME = 150
const BASE_URI = 'http://localhost:8000';

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
        throw `HTTP Exception Status: ${response.status}`
    };
    return await response.json();
}

const marvel = () => {
    return {
        mode: null,
        characterLoaded: false,
        comicLoaded: false,
        affiliateLoaded: false,
        itemsLoaded: false,
        discoveredLoaded: false,
        characterSearch: '',
        character: {},
        comic: {},
        comics: [],
        affiliate: {},
        affiliates: [],
        discovered: [],
        async clearCharacter() {
            this.characterLoaded = false;
            this.comicLoaded = false;
            this.affiliateLoaded = false;
            this.itemsLoaded = false;
            this.characterSearch = '';
            await asyncTimeout(FADE_TIME);  // Allow for fade animation.
            this.mode = null;
            this.character = {};
            this.comic = {};
            this.comics = [];
            this.affiliate = {};
            this.affiliates = [];
        },
        async getCharacterByName() {
            if (!this.characterSearch) return;
            const characterSearch = this.characterSearch;
            await this.clearCharacter();
            this.character = await sendAsyncRequest('GET', `/api/v1/character?name=${characterSearch}`);
        },
        async getComicsByCharacter() {
            this.itemsLoaded = false;
            await asyncTimeout(FADE_TIME);
            this.mode = 'comics';
            if (this.comics.length == 0) {
                const response = await sendAsyncRequest('GET', `/api/v1/comics/character/${this.character.marvel_id}`);
                this.comics = Object.values(response);
            }
            this.character.has_comics = true;
            this.itemsLoaded = true;
        },
        async getAffiliatesByCharacter() {
            this.itemsLoaded = false;
            await asyncTimeout(FADE_TIME);
            this.mode = 'affiliates';
            if (this.affiliates.length == 0) {
                const response = await sendAsyncRequest('GET', `/api/v1/character/${this.character.marvel_id}/affiliates`);
                this.affiliates = Object.values(response);
                this.getDiscoveredCharacters()
            }
            this.itemsLoaded = true;
        },
        async getDiscoveredCharacters() {
            this.discoveredLoaded = false;
            await asyncTimeout(FADE_TIME);
            this.discovered = await sendAsyncRequest('GET', '/api/v1/characters/discovered');
            this.discoveredLoaded = true;
        },
        async getComicDetail(comic) {
            if (this.comic.marvel_id === comic.marvel_id) return;
            this.comicLoaded = false;
            await asyncTimeout(FADE_TIME);
            this.comic = comic;
        },
        async getAffiliateDetail(affiliate) {
            if (this.affiliate.marvel_id === affiliate.marvel_id) return;
            this.affiliateLoaded = false;
            await asyncTimeout(FADE_TIME);
            this.affiliate = affiliate;
        },
        async setCharacter(character) {
            if (this.character.marvel_id == character.marvel_id) return;
            await this.clearCharacter();
            this.character = character;
        }
    };
}
