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
  $('#log-form').css("display", "block");
}

$('#log').on('click', showLogForm);

// show info page in sidebar 
function showInfoPage() {
  
  $('#log-info > div').replaceWith('<div><ul><p>PHOTO COMMENT</p></ul></div>');
}

$('#info').on('click', showInfoPage);

// submit log to user profile 
function sendAlert(alertMsg) {
  alert(alertMsg);
}

function submitArtLog(evt) {
  evt.preventDefault();
  console.log("YOU GOT TO THE EVENT PREVENT DEFAULT")
  const artId = 1000
  console.log(artId)

  const formData = new FormData($('#log-form'));
  formData.append('image', $('input[type=file]')[0].files[0]);
  formData.append('comment', $('#comment').val())


const opts = {
  async: false,
  type: "POST",
  url: '/log/' + artId,
  data: formData,
  processData: false,
  contentType: false,
  success: sendAlert
}

  console.log(formData);
  console.log('POST /info for log');

  $.ajax(opts);
}

$('#log-form').on('submit', submitArtLog);
