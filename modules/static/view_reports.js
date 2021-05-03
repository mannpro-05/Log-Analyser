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


$(document).ready(function() {


    window.onclick = function(event) {
        if (!event.target.matches('.dropdownbutton')) {

            $(".dropdown-content").each(function(){
                $(this).hide();
            });
        }
    }

    console.log("Ready");
});



function dropdownControl(downloadDropdown){
    $(downloadDropdown).parent().find(".dropdown-content").toggle("show");
}

function downloadReport(downloadButton,format){
    var data = {
        "title": $(downloadButton).closest("tr").find(".reportTitle").text(),
        "fileType": format
    }

    console.log("Download: ",data);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'text/csv',
        url: '/download',
    })
}

function deleteReport(deleteButton){
    var data = {
        "title": $(deleteButton).closest("tr").find(".reportTitle").text()
    }

    console.log("Delete: ",data);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: '/deleteReport',
    }).done(function (data) {
        $(deleteButton).parents("tr").remove();
        alert(data.message);
    });

}