$(function () {

    // ajax za obisk glede na role
$(document).ready(function(){

    $.ajax({

            type: "GET",
            url: "/visit_list/",
            data: {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: planVisitSuccess,
            dataType: 'html'
        });


        $('#confirm_plan').click(function(e){
        e.preventDefault();
        alert("Confirm Plan");
        $("#id_plan_list").each(function(){
            $(this).prop('selected',true);
        });
        	var form = $(this).parents('form');
        	form.submit();



});

    //master detail delovni nalog MS
    $('#plan_detail').on('click', function (e) {
        //alert("Neopravljeni "+$('#visit_list option:selected').val()+' Opravljeni '+$('#id_plan_list option:selected').val());
        var selected_data;
        if($('#visit_list option:selected').val()!=undefined){
            //alert("NOT nULL");
            selected_data = $('#visit_list option:selected').val();
        }else if($('#id_plan_list option:selected').val() != undefined){
            selected_data = $('#id_plan_list option:selected').val();

        }else{
            alert("Ni izbran noben obisk");
            e.preventDefault();
        }
        selected_data = String(selected_data);
        selected_data=selected_data.split(' ');
        //selected_data=selected_data[0];
        //alert("Klick registered  "+ selected_data);
        $.ajax({
            type: "POST",
            url: "/plan_detail/",
            data: {
                'visit_list': selected_data[1],//'3 | Mislejeva',
                //'obisk_id' : selected_data[0],
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
    //filter plan glede na dan
    $("#filter_plan").on('click',function(){

        //alert("Prebran datum: "+$("#date_picker").val());

        $.ajax({

            type: "POST",
            url: "/visit_list/",
            data: {
                'datum' : String($("#date_picker").val()),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: planVisitSuccess,
            dataType: 'html'
        });

    });

    //Obvezne obiske dodaj v plan
    $( document ).ajaxStop(function() {
     // alert("Document is ready ajax");
        //parse the value
      $("#visit_list > option").each(function () {
        var plan_data = plan_data = $(this).val().split(' ');
        var plan_option =$(this).text().split('\\t');
        //alert(/\t/ +"This is data updated: "+plan_data.indexOf(/\t/));
          //alert("values: "+plan_data+"\ntext: "+plan_option[0]);


        //alert("Datum: "+plan_data[3] +' mandadatory date: '+ mandatoryDate(plan_data[3]));
        if(plan_data[2] == "Obvezen" && mandatoryDate(plan_data[3])) {
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
    //alert("SUCCESS visitl list");
    $.ajax({

            type: "GET",
            url: "/planned_list/",
            data: {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: plannedListSuccess,
            dataType: 'html'
        });
}


function planDetailSuccess(data, textStatus, jqXHR) {
    $('.modal-body').html(data);
}
function plannedListSuccess(data, textStatus, jqXHR) {
    $('#id_plan_list').html(data);
}


function mandatoryDate(datum) {
    //alert("inside datum "+datum);
    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate()+1);
	var day1 = tomorrow.getDate();
	var month1 = (tomorrow.getMonth()+1);
	var year1 = tomorrow.getFullYear();
   // alert("inside datum ");

	if(datum ==''){
	    alert("Datum je prazenk");
		return false;
	}
    //alert("inside datum  2");
	var mandatory = datum.split(".");
	//alert("tomorrow:"+firstVisit[2]);
	/*if(mandatory[2]<year1){
		return false;
	}
	if(mandatory[2]==year1 && mandatory[1]<month1){
		return false;
	}
    */
	//alert("inside datum "+mandatory);
	if(mandatory[2] == year1 && mandatory[1] == month1 && mandatory[0] == day1){
		//alert("datum matches with tomorrow!");

		return true;
	}
    return false;
}