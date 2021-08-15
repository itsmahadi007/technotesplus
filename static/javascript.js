const burgerIcon = document.querySelector('#burger');
const navberMenu = document.querySelector('#nav-links');
const add_new = document.querySelector('#add_new');


burgerIcon.addEventListener('click', () => {
    navberMenu.classList.toggle('is-active');
});

add_new.addEventListener('click', () => {

    document.getElementById("hide1").style.display = "none";
    document.getElementById("hide2").style.display = "none";
    document.getElementById("hide3").style.display = "none";
    document.getElementById("note_id").value = "null";
    var elements = [];
    elements = document.getElementsByClassName("tobe_clear");

    for (var i = 0; i < elements.length; i++) {
        elements[i].value = "";
    }

});


const share = document.querySelector('#hide2');
const model = document.querySelector('#modal');
const model_background = document.querySelector('.modal-background');
const del = document.querySelector('.delete');
share.addEventListener('click', () => {
    model.classList.add('is-active');
});

model_background.addEventListener('click', () => {
    model.classList.remove('is-active');
});
del.addEventListener('click', () => {
    model.classList.remove('is-active');
});

// const search_text = document.querySelector('#search_text');
// $("#search_button").click(function () {
//     let serialization = $('#search_form').serialize();
//     console.log(serialization)
//     console.log(search_text.value)
//
//     $.ajax({
//         url: '/technote/' + search_text.value,
//         type: 'get',
//         success: function (response) {
//             console.log('searched_note')
//         }
//     })
// });





