"use-strict"

$.get('/logs.json', (response) => {
    $('#greeting').html(response.username);

})

$.get('/logs.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const log = myArray[i];
        $('#profile-log-row').append('<div class="grid-item" id="row>"><img class="grid-item" src=' + log.image + '></img><span class="grid-item" id="comment">' + 'Comment:' + log.comment + '</span><br></div>');
    }
})

$.get('/adds.json', (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const add = myArray[i];
        $('#profile-add-row').append('<div class="grid-item" id="row"><img class="grid-item" src=' + add.image + '></img><span class="grid-item" id="title">' + 'Title:' + add.title + '</span><span class="grid-item" id="hint">' + 'Hint:' + add.hint + '</span><br></div>');
    }
})