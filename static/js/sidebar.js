"use-strict"

// logic to close sidebar when click clse button 
$('#closebtn').on('click', function (evt) {
  $('#Sidebar').css("width", "0");
});

// show the art title, artist, and hint in the sidebar 
function showArtInfo(response) {

  $('#hint').html(response.hint);
  $('#title').html(response.title);
  $('#artist').html(response.artist);
  $('#art-id').html(response.art_id);
}

function handleInfoEvent(evt) {
  evt.preventDefault();

  const artId = evt.features[0].properties.art_id
  $.get('/art/' + artId, showArtInfo);
}

map.on('click', 'art-point', handleInfoEvent);

// show log form in sidebar  
function showLogForm() {
  const x = $('#log-form');
  const displaySetting = x[0].style.display;
  if (x[0].style.display === "block") {
    x[0].style.display = "none";
  } else {
    x[0].style.display = "block";
  }
}

$('#log').on('click', showLogForm);

// show info page in sidebar 
function showInfoPage() {
  var x = $('#user-logs');
  var displaysetting = x[0].style.display;
  if (x[0].style.display === "block") {
    x[0].style.display = "none";
  } else {
    x[0].style.display = "block";
  }

  const artId = $('#art-id').text()

  $.get('/art_logs/' + artId, (response) => {
    let myArray = response.logs 
    for (let i = 0; i < myArray.length; i++) {
        const log = myArray[i];
        $('#log-info').append('<div><img id="art-log-img" src=' + log.image + '></img><span id="comment">' + log.comment + '</span><br></div>');
        }
    })
  }

$('#info').on('click', showInfoPage);

// submit log to user profile 
function sendAlert(alertMsg) {

  alert(alertMsg);
  // clears form on submit 
  $('#log-form').children('input[type="text"]').val('');
  $('#log-form').children('input[type="file"]').val('');
}

function submitArtLog(evt) {

  evt.preventDefault();

  const artId = $('#art-id').text()

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
