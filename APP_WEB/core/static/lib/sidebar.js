let floatButton = document.getElementById('expand-side-bar');

floatButton.addEventListener('click', () => {

    let sidebar = document.getElementById('sidebar');

    if (sidebar.classList.contains('to-left')) {
        sidebar.classList.remove('to-left')
    } else {
        sidebar.classList.add('to-left')
    }

})

document.querySelectorAll("img.svg").forEach(img => {
    let imgURL = img.getAttribute("src")

    fetch(imgURL)
        .then(response => {
            response.text()
                .then(svg => {
                    const svgElement = new DOMParser().parseFromString(svg, "image/svg+xml")
                    img.replaceWith(svgElement.documentElement)
                })
        })
})