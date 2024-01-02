const toggleMenu = () => {
    const menu = document.getElementById('menu')
    menu.classList.toggle('hidden')
}

const dropdownList = document.getElementById('dropdownList')
const dropdownButton = document.getElementById('dropdownButton')

dropdownButton.addEventListener('click', (event) => {
    event.stopPropagation()
    dropdownList.classList.toggle('hidden')
})

document.documentElement.addEventListener('click', () => {
    if (!dropdownList.classList.contains('hidden')) {
        dropdownList.classList.toggle('hidden')
    }
})