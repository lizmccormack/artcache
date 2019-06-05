"use-strict"

$.get('/profile.json', (response) => {
    $('#greeting').html(response.username);
})