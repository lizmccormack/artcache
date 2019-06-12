"use-strict"

// logic to close sidebar when click clse button 
$('#sidebar-close-btn').on('click', function (evt) {
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
    console.log(response);
    let myArray = response.logs 
    console.log(myArray);
    if (myArray.length < 1) {
      $('#user-logs').html('<p>not logged yet</p>')
      console.log("hellooooo");
    } else {
      for (let i = 0; i < myArray.length; i++) {
          const log = myArray[i];
          $('#user-logs').html('<div><img id="art-log-img" src=' + log.image + '></img><span id="comment">' + log.comment + '</span><br></div>');
          }
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
