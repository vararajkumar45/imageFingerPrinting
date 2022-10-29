function uploadValidate() {
    if(image.value == '') {
        image.style.border = '2px solid red';
        imageError.style.display = 'block';
        return false;
    } else {
        image.style.border = '2px solid #ccc';
        imageError.style.display = 'none';
    }
}

function searchValidate() {
    if(image_type.value == "") {
        image_type.style.border = '2px solid red';
        searchError.style.display = 'block';
        return false;
    } else {
        image_type.style.border = '2px solid #ccc';
        searchError.style.display = 'none';
    }
}

let image = document.getElementById('image');
let imageError = document.getElementById('imageError');
let image_type = document.getElementById('image_type');
let searchError = document.getElementById('imageTypeError');

let preloader = document.getElementById('preloader');
window.addEventListener('load', function() {
    preloader.style.display = 'none';
});