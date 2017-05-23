$(function () {

    // ajax za obisk glede na role
$(document).ready(function(){

   $.ajax({

            type: "POST",
            url: "/nurseList/",
            data: {
                'search_nurse' : String($("#search_nurse").val()),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: nurseListSuccess,
            dataType: 'html'
        });

});


    $('#nurse_sub').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/subNurseList/",
            data: {
                'search_nurse' : String($("#search_nurse").val()),
                'nurse_sub' : String($("#nurse_sub").val()),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: subNurseSuccess,
            dataType: 'html'
        });
    });

    //validacija preden se pošljejo podatki

    $('#confirm_nurse').click(function(e){
        //alert("Confirm Nurse");
            e.preventDefault();
        if(dateValidation(String($("#start_date").val()),String($("#end_date").val()))){
            	var form = $(this).parents('form');
        	    form.submit();
        }/*else{

            sweetAlert("Hello","date validation is false","warning");
        }*/
        //alert("AFTER IF");

        });

});


function nurseListSuccess(data, textStatus, jqXHR) {
    $('#nurse_list').html(data);
}


function subNurseSuccess(data, textStatus, jqXHR) {
    $('#nurse_sub_list').html(data);
}

function dateValidation(datum1,datum2) {
    //alert("inside datum "+datum);
    var today = new Date();
    //today.setDate(today.getDate());
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();
    //alert("inside datum "+datum1+"    "+datum2);

	if(datum1 ==''){
	   // alert("Datum je prazen");
	   sweetAlert("Napaka","Datum začetka nadomeščanja ni izpolnjen","error");
		return false;
	}
	if(datum2 ==''){
	   sweetAlert("Napaka","Datum konca nadomeščanja ni izpolnjen","error");
		return false;
	}
    //alert("inside datum  2");
	var date_from = datum1.split(".");
	var date_to =datum2.split(".");
	// alert("SPLIT VALUES "+date_from+"    "+date_to);
	//alert("today:"+firstVisit[2]);
	//start date vs today
	if(date_from[2]<year1){
	 sweetAlert("Napaka","Datum začetka nadomeščanja ne more biti v preteklosti","error");
		return false;
	}
	if(date_from[2]==year1 && date_from[1]<month1){
	 sweetAlert("Napaka","Datum začetka nadomeščanja ne more biti v preteklosti","error");
		return false;
	}


	if(date_from[2] == year1 && date_from[1] == month1 && date_from[0] < day1){
		sweetAlert("Napaka","Datum začetka nadomeščanja ne more biti v preteklosti","error");
		return false;
	}
	//end date vs today
	if(date_to[2]<year1){
	    sweetAlert("Napaka","Datum konca nadomeščanja ne more biti v preteklosti","error");
		return false;
	}
	if(date_to[2]==year1 && date_to[1]<month1){
	    sweetAlert("Napaka","Datum konca nadomeščanja ne more biti v preteklosti","error");
		return false;
	}

	//alert("inside datum "+mandatory);
	if(date_to[2] == year1 && date_to[1] == month1 && date_to[0] < day1){
		sweetAlert("Napaka","Datum konca nadomeščanja ne more biti v preteklosti","error");

		return false;
	}

	//start vs end
	//year
	if(date_to[2]<date_from[2]){
	 sweetAlert("Napaka","Datum konca nadomeščanja ne more biti manjši od začetnega","error");
		return false;
	}
	//month
	if(date_to[2]==date_from[2] && date_to[1]<date_from[1]){
	    sweetAlert("Napaka","Datum konca nadomeščanja ne more biti manjši od začetnega","error");
		return false;
	}

	//day
	if(date_to[2] == date_from[2] && date_to[1] == date_from[1] && date_to[0] < date_from[0]){
	    sweetAlert("Napaka","Datum konca nadomeščanja ne more biti manjši od začetnega","error");

		return false;
	}

    return true;
}
