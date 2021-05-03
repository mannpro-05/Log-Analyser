// --------------------------------navigation-----------------------------------------
function navControl() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}
// --------------------------------navigation-----------------------------------------


function sendQuery(){
    var data = {
        "subject" : $("#subject").val(),
        "body" : $("#message").val()
    }
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/sendQuery'

    }).done(function (data) {
        alert(data.message);
    })
}