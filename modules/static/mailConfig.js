function mailConfig(){

    var data = {
        "MAIL_PORT" : $("#mailPort").val(),
        "MAIL_SERVER" : $("#mailServer").val(),
        "MAIL_USERNAME" : $("#mailUsername").val(),
        "MAIL_PASSWORD" : $("#password").val(),
        "MAIL_USE_SSL" : $("#ssl").val()
    }
    alert('hi');
    console.log(data)
     $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/mailConfig'

    }).done(function (data) {
        alert(data.message);
    })
}