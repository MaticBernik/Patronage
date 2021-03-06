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

    //bolezen
    $('#search_illness').keyup(function () {
       // alert("Bolezen: "+$('#search_illness').val());
        $.ajax({
            type: "POST",
            url: "/illness_list/",
            data: {
                'illness_list': $('#search_illness').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchIllnessSuccess,
            dataType: 'html'
        });
    });

    $('#searchPatient').keyup(function () {
        //preveri če je pacient že v listi
        var added_patient = '';

            added_patient = $('#id_addPatient').find("option:first-child").val();
            if(added_patient != undefined){
                added_patient=added_patient.split(' ');
                added_patient = added_patient[0];
               // alert("AJAX FIRST SELECTED PATIENT IS: "+added_patient);
            }else{
                added_patient ='';
            }
            //alert("added patient value: "+added_patient);
        $.ajax({
            type: "POST",
            url: "/patient/search/",
            data: {
                'search_patient': $('#searchPatient').val(),
                'added_patient' : added_patient,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchPatientSuccess,
            dataType: 'html'
        });
    });
    // ajax za obisk glede na role
/*
$(document).ready(function(){


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

});


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

    //posta autocomplete

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


    $('#searchPatient').on('change', function () {
        //alert("Pozdrav iz patienta");
        var input_value = String($('#searchPatient').val());
        var name_regex ="^[0-9]{12} [A-Z\u010C\u0160\u017d\u0106\u0110\a-z\u010d\u0161\u017e\u0107\u0111]+";

        var nameRE = new RegExp(name_regex);
        //alert("Pozdrav iz patienta reges");
        //alert("Pozdrav iz patienta");
        if(input_value.match(name_regex) == null){
            alert("Napačen format imena");
            input_value='';

        }else{
            input_value=input_value.split(' ');
            input_value=input_value[0];
        }
        //alert("Pozdrav after if");

       // alert("from health visitorInput has changed "+input_value[0]);

        $.ajax({
            type: "POST",
            url: "/health_visitor/",
            data: {
                'patient_id': input_value,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: chooseSisterSuccess,
            dataType: 'html'
        });

    });

    //unselect the first list
    $("#id_plan_list").on('change',function(){


        //alert("BEFORE");
        $("#visit_list > option").prop('selected',false);
        //alert("AFTER");

    });

    //unselect the second list
    $("#visit_list").on('change',function(){


        //alert("BEFORE");
        $("#id_plan_list > option").prop('selected',false);
        //alert("AFTER");

    });

    //Obvezne obiske dodaj v plan
    $( document ).ajaxStop(function() {
     // alert("Document is ready ajax");
        //parse the value
      $("#visit_list > option").each(function () {
        var plan_data = $(this).val().split(' ');
        var plan_option =$(this).text().split('\\t');
        //alert(/\t/ +"This is data updated: "+plan_data.indexOf(/\t/));
          //alert("values: "+plan_data+"\ntext: "+plan_option[0]);



        if(plan_data[2] == "True") {
          //alert("This is data: "+plan_data[1]);
           $(this).remove().appendTo("#id_plan_list");
         }
           // $(this).remove().appendTo("#id_plan_list");
            //rearrangeList("#list2");
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
        //add required atribute
        $('#id_cureId').prop('required',true);
        $('#id_addPatient').prop('required',false);
        $('#id_materialDN').prop('required',false);
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
/*
function chooseRoleSuccess(data, textStatus, jqXHR) {
    $('#choose-visit').html(data);
}
*/
function searchIllnessSuccess(data, textStatus, jqXHR) {
     $('#illness_list').html(data);
}

function chooseSisterSuccess(data, textStatus, jqXHR) {
     $('#id_nurse_id').html(data);
}