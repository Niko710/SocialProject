const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minHeight = 250;
const minWidth = 250;

let head = document.getElementsByTagName('head')[0];
let link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);

let body = document.getElementsByTagName('body')[0]
let boxHTML = `
<div id='bookmarklet'>
    <a href="#" id='close'>&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class='images'></div>
</div>
`
body.innerHTML += boxHTML

function bookmarkletLaunch () {
    let bookmarklet = document.getElementById('bookmarklet')
    let imagesFound = bookmarklet.querySelector('.images')

    imagesFound.innerHTML = ''

    bookmarklet.style.display = 'block'

    bookmarklet.querySelector('#close').addEventListener('click', () => {
        bookmarklet.style.display = 'none'
    })

    let images = document.querySelectorAll("img[src$='.png'], img[src$='.jpg'], img[src$='.jpeg']")
    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            let imageFound = document.createElement('img')
            imageFound.src = image.src
            imagesFound.append(imageFound)
        }
    })

    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', event => {
            let imageSelected = event.target
            bookmarklet.style.display = 'none'
            window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title), '_blank')
        })
    })
}

bookmarkletLaunch()

