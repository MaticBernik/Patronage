$(function () {

    $('#medicine').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/medicine/search/",
            data: {
                'search_text' : $('#medicine').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });

     $('#searchPatient').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/patient/search/",
            data: {
                'search_patient' : $('#searchPatient').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchPatientSuccess,
            dataType: 'html'
        });
    });

     //master detail obiski
    $('#choose-visit').on('change',function () {

        $.ajax({
            type: "POST",
            url: "/visit/choice/",
            data: {
                'choose_visit' : $('#choose-visit').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },

            success: chooseVisitSuccess,
            dataType: 'html'
        });

    });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}
function searchPatientSuccess(data, textStatus, jqXHR) {
     $('#patientsList').html(data);
}
function chooseVisitSuccess(data, textStatus, jqXHR) {
     $('#visitType').html(data);
    // alert('from ajax '+$("#visitType").find("option:first-child").val());

     if($("#visitType").find("option:first-child").val() == "Aplikacija injekcij"){
         //prikazi opcijo za izbiro zdravil
         $('#cureId').show();
		}
     /*alert('select the data')
     $('#visitType option:first-child').attr("selected", "selected");*/
}