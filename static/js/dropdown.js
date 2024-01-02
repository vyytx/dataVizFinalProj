const dropdownMenu = document.getElementById('dropdownMenu')
const dropdownButton = document.getElementById('dropdownButton')
const dropdownSearch = document.getElementById('dropdownSearch')
const dropdownList = document.getElementById('dropdownList')

dropdownButton.addEventListener('click', (event) => {
    event.stopPropagation()
    dropdownMenu.classList.toggle('hidden')
})

document.documentElement.addEventListener('click', (event) => {
    if (!dropdownMenu.classList.contains('hidden') && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.toggle('hidden')
    }
})

dropdownSearch.addEventListener('input', () => {
    const inputText = dropdownSearch.value
    const searchText = inputText.replace('台', '臺').toLowerCase()

    const listItems = dropdownList.getElementsByTagName('li')
    for (const listItem of listItems) {
        const anchor = listItem.querySelector('a')
        if (!anchor.innerText.toLowerCase().includes(searchText)) {
          listItem.classList.add('hidden')
        } else {
          listItem.classList.remove('hidden')
        }
      }
})