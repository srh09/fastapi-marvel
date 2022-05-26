const sayHi = () => console.log('Hi there------')
const sayBye = () => console.log('goodbye-----')

let mCharacter = {
    'id': 12345,
    'name': 'Spectrum',
    'description': 'Nice and thorough description of Spectrum',
    'picture': null
}

const logo = document.getElementById('logo-svg')
logo.addEventListener('mouseenter', () => {
    logo.style.animation = "runAway 8s"
})
logo.addEventListener('animationend', () => {
    logo.style.animation = null;
})
