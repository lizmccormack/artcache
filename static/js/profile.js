"use-strict"

$.get('/logs.json', (response) => {
    $('#greeting').html(response.username);

})

$.get('/logs.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const log = myArray[i];
        $('#log').append('<div class="row>"><img src=' + log.image + '></img><span id="comment">' + 'Comment:' + log.comment + '</span><br></div>');
    }
})

$.get('/adds.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const add = myArray[i];
        $('#add').append('<div class="row"><img src=' + add.image + '></img><span id="title">' + 'Title:' + add.title + '</span><span id="hint">' + 'Hint:' + add.hint + '</span><br></div>');
    }
})