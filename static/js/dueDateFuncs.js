function activateGcal() {
    window.open("https://accounts.google.com/o/oauth2/auth?client_id=977810044263-vk1r3up83p2ducal2887bpa4d3fa7flm.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&access_type=offline&response_type=code", "_blank");
    $('#modal1').modal('open');
}

function activateEmail() {
    $('#modal2').modal('open');
}

$(document).ready(function(){
    $('.modal').modal();
});
