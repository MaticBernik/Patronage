$(function () {

    // ajax za obisk glede na role
$(document).ready(function(){
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

    //master detail delovni nalog MS
    $('#plan_detail').on('click', function (e) {
        //alert("THIS WOKRS");
        var selected_data;
        if($('#visit_list').val()!=''){
            selected_data = $('#visit_list').val();
        }else if($('#id_plan_list').val() != ''){
            selected_data = $('#id_plan_list').val();
        }else{
            alert("Ni izbran noben obisk");
            e.preventDefault();
        }
        selected_data = String(selected_data);
        selected_data=selected_data.split(' ');
        //selected_data=selected_data[0];
        alert("Klick registered  "+ selected_data);
        $.ajax({
            type: "POST",
            url: "/plan_detail/",
            data: {
                'visit_list': selected_data[1],//'3 | Mislejeva',
                'obisk_id' : selected_data[0],
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: planDetailSuccess,
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


function planVisitSuccess(data, textStatus, jqXHR) {
    $('#visit_list').html(data);
}


function planDetailSuccess(data, textStatus, jqXHR) {
    $('.modal-body').html(data);
}
