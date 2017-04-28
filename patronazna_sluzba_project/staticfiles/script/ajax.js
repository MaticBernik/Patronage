$(function () {
    $('#medicine').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/medicine/search/",
            data: {
                'search_text': $('#medicine').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
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
                'search_patient': $('#searchPatient').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchPatientSuccess,
            dataType: 'html'
        });
    });
    // ajax za obisk glede na role
$(document).ready(function(){
   // alert("TEST FOR AJAX");

     $.ajax({

            type: "GET",
            url: "/visit/role/",
            data: {
                'choose_visit': $('#choose-visit').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: chooseRoleSuccess,
            dataType: 'html'
        });

     //second AJAX
    //alert("Second AJAX MS");
      $.ajax({

            type: "GET",
            url: "/visit_list/",
            data: {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: planVisitSuccess,
            dataType: 'html'
        });
});
/*

*/
    //master detail obiski
    $('#choose-visit').on('change', function () {

        $.ajax({
            type: "POST",
            url: "/visit/choice/",
            data: {
                'choose_visit': $('#choose-visit').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: chooseVisitSuccess,
            dataType: 'html'
        });

    });

    //post autocomplete

    $('#search_post').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/post/",
            data: {
                'search_post': $('#search_post').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchPostSuccess,
            dataType: 'html'
        });
    });

    //district autocomplete

    $('#search_district').keyup(function () {
        //alert("KEyup event form okolis")
        $.ajax({
            type: "POST",
            url: "/district/",
            data: {
                'search_post': $('#search_post').val(),
                'search_district': $('#search_district').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchDistrictSuccess,
            dataType: 'html'
        });
    });

    //master detail delovni nalog MS
    $('#plan_detail').on('click', function () {
        var selected_data = $('#visit_list').val();
        alert("Klick registered  data"+ data);
        $.ajax({
            type: "POST",
            url: "/plan_detail/",
            data: {
                'donkey': selected_data,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: planDetailSuccess,
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

    if ($("#visitType").find("option:first-child").val() == "Aplikacija injekcij") {
        //prikazi opcijo za izbiro zdravil
        $('#cureId').show();
    }
    /*alert('select the data')
     $('#visitType option:first-child').attr("selected", "selected");*/
}
function searchPostSuccess(data, textStatus, jqXHR) {
    $('#post_codes').html(data);
}

function searchDistrictSuccess(data, textStatus, jqXHR) {
    $('#district_name').html(data);
}

function chooseRoleSuccess(data, textStatus, jqXHR) {
    $('#choose-visit').html(data);
}


function planVisitSuccess(data, textStatus, jqXHR) {
    $('#visit_list').html(data);
}


function planDetailSuccess(data, textStatus, jqXHR) {
    $('.modal-body').html(data);
}
