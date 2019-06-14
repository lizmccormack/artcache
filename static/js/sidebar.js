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
  console.log(response.img);
  console.log(response.source);

  if (response.source === 'user') {
    $('#show-image').show(); 
  } else {
    $('#show-image').hide(); 
  }
}

function handleInfoEvent(evt) {
  evt.preventDefault();

  const artId = evt.features[0].properties.art_id
  $.get('/art/' + artId, showArtInfo);
}

map.on('click', 'art-point', handleInfoEvent);

// modal for picture

function showPictureModal(response) {

   $('#image-modal').css('display', 'block');
   $('#art-img').attr('src', response.img);
   console.log(response.img);
}

function handlePictureEvent(evt) {
  evt.preventDefault();

  const artId = $('#art-id').text()
  $.get('/art/' + artId, showPictureModal);
}

$('#show-image').on('mouseover', handlePictureEvent)

const span_img = $('#close-btn-img')[0];
console.log(span_img);

$('#close-btn-img').on('click', function() {
    $('#image-modal').css("display", "none");
})
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
    } else {
      html = ''
      let li = '<li>'
      for (let i = 0; i < myArray.length; i++) {
             const log = myArray[i];
             console.log(log);
             li += '<div class="grid-contaner"><img class="grid-item" id="art-log-img" src=' + log.image + '></img><span class="grid-item" id="comment">' + log.comment + '</span></div>'
            };
            li + '</li>'
            $('#user-logs').html(li);
          };
        })
      }

$('#info').on('click', showInfoPage);

// submit log to user profile 
function sendAlert(alertMsg) {

  alert(alertMsg);
  // clears form on submit 
  $('#log-form').children('textarea').val('');
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
