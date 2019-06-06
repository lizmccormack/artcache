"use-strict"

$.get('/logs.json', (response) => {
    $('#greeting').html(response.username);

})

$.get('/logs.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const log = myArray[i];
        $('#log').append('<img src=' + log.image + '></img><span id="comment">' + log.comment + '</span><br>');
    }
})

$.get('/adds.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const add = myArray[i];
        $('#add').append('<img src=' + add.image + '></img><span id="title">' + add.title + '</span><span id="hint">' + add.hint + '</span><br>');
    }
})