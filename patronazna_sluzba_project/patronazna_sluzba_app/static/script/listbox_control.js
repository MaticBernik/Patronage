$(function () {
    //for each in visit_list that is true add it ro id_plan_list


    $("#add_plan").click(function () {
       // alert("BEFORE");
        var plan_date = String($("#id_plan_list").find("option:first-child").val());
        plan_date = plan_date.split(' ');
        plan_date = plan_date [3];
        //
        // alert("AFTER "+plan_date );
        if(editPossible(plan_date)){
             $("#visit_list > option:selected").each(function () {
                $(this).remove().appendTo("#id_plan_list");
                //rearrangeList("#list2");
            });
        }

    });

    $("#remove_plan").click(function (e) {
       // alert("BEFORE");
        var plan_date = String($("#id_plan_list").find("option:first-child").val());
        plan_date = plan_date.split(' ');
        plan_date = plan_date [3];
        //alert("AFTER "+plan_date );
        if(editPossible(plan_date)){
            $("#id_plan_list > option:selected").each(function () {
           // alert("Odstrani izbrano opcijo");
            //alert("Opcija: "+$(this).text().indexOf('Obvezen'));
                plan_date = String($(this).val()).split(' ');
                 plan_date = plan_date [3];
            if((($(this).val().indexOf('Obvezen'))>-1) && mandatoryDate(plan_date)){
                sweetAlert("Popravljanje plana ni mogoče", "Datum obiska je obvezen "+plan_date, "error");
                //alert("Datum obiska je obvezen");
                e.preventDefault();
            }else{
                $(this).remove().appendTo("#visit_list");
            }

            //rearrangeList("#list1");
        });
        }

    });

});

function editPossible(datum) {
    //alert("inside datum "+datum);
    var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();
   // alert("inside datum ");
    //alert("inside datum  2");
	var editable = datum.split(".");
	//alert("tomorrow:"+firstVisit[2]);
	if(editable[2]<year1){
	    sweetAlert("Popravljanje plana ni mogoče", "Datum plana mora biti enak ali večji od današnjega!", "error");
	     //alert("Popravljanje plana ni mogoče, datum plana mora biti enak ali večji od današnjega!");
		return false;
	}
	if(editable[2]==year1 && editable[1]<month1){
	    sweetAlert("Popravljanje plana ni mogoče", "Datum plana mora biti enak ali večji od današnjega!", "error");
        //alert("Popravljanje plana ni mogoče, datum plana mora biti enak ali večji od današnjega!");
		return false;
	}

	//alert("inside datum "+mandatory);
	if(editable[2] == year1 && editable[1] == month1 && editable[0] < day1){
		//alert("datum matches with tomorrow!");
        sweetAlert("Popravljanje plana ni mogoče", "Datum plana mora biti enak ali večji od današnjega!", "error");
         //alert(", datum plana mora biti enak ali večji od današnjega!");
		return false;
	}
    return true;
}