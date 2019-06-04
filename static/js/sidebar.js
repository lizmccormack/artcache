"use-strict"

$('#closebtn').on('click', function (evt) {
  $('#Sidebar').css("width", "0");
});

// show the art hint in the sidebar 
function showArtInfo(response) {

  $('#hint').html(response.hint);
  $('#title').html(response.title);
  $('#artist').html(response.artist);
}

function handleInfoEvent(evt) {
  evt.preventDefault();

  const artId = evt.features[0].properties.art_id
  $.get('/art/' + artId, showArtInfo);
}

map.on('click', 'art-point', handleInfoEvent);

// show log form in sidebar  
function showLogForm() {

  $('#log-info > div').replaceWith('<div><form action="/log/<art_id>" id="log-form" methods="POST"><input type="file" name="image"></input><br><input type="text" name="comment"></input><br><input type="submit" value="submit"></form></div>');
}

$('#log').on('click', showLogForm);

// show info page in sidebar 
function showInfoPage() {
  
  $('#log-info > div').replaceWith('<div><ul><p>PHOTO COMMENT</p></ul></div>');
}

$('#info').on('click', showInfoPage);

// submit log to user profile 
function submitArtLog(evt) {
  evt.preventDefualt();

  const artId = evt.features[0].properties.art_id
  console.log(artId)

  const formData = {
    image: $('#image').val(),
    comment: $('#comment').val()
}

  console.log('POST /info for log');

  $.post('/log/' + artId, formData, callbackfunction)
}
