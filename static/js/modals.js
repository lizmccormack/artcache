"user-strict"

const modal = $('#info-modal');
console.log(modal);
const span = $('#close-btn')[0];
console.log(span);

$('#site-info').on('click', function() {
    $('#info-modal').css("display", "block");
})

$('#close-btn').on('click', function() {
    $('#info-modal').css("display", "none");
})

