
function task_validation(){
    //alert("Hello this is task validator");
    //$("#confirm").removeAttr('disabled');
	var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();

	var datum = document.getElementById('visitDate');

	//prvi datum obiska
	if(datum.value ==''){
	    alert("Datum prvega obiska je obvezen podatek");
	    swal("Napaka", "Datum prvega obiska je obvezen podatek", "error");
		return false;
	}
	var message = document.getElementById('message');

	var firstVisit = datum.value.split(".");
	//alert("today:"+firstVisit[2]);
	if(firstVisit[2]<year1){
		alert("Napacno letnico");
		//$("#confirm").attr('disabled','disabled');
		return false;
	}
	if(firstVisit[2]==year1 && firstVisit[1]<month1){
		alert("Napacen datum! Datum obiska mora biti vecji od trenutnega!");
		//$("#confirm").attr('disabled','disabled');
		return false;
	}

	if(firstVisit[2] == year1 && firstVisit[1] == month1 && firstVisit[0] <= day1){
		alert("Napacen datum! Datum obiska mora biti vecji od trenutnega!");
		//$("#confirm").attr('disabled','disabled');
		return false;
	}

	var visit_count  = document.getElementById('id_visitCount').value;
	var time_interval = document.getElementById('timeInterval').value;
	var time_period = document.getElementById('timePeriod').value;
	var patient_name = document.getElementById('searchPatient').value;
	var illness = document.getElementById('search_illness').value;
	var visit_type = document.getElementById('choose-visit').value;
	var visit_type_detail = document.getElementById('visitType').value;

	if(visit_type ==''){
	    alert("Ni izbrana vrsta obiska!");

		return false;
	}

	if(visit_type_detail ==''){
	    alert("Ni izbrana podvrsta obiska!");

		return false;
	}

	var patient_num =0 ;
        	if(visit_type_detail =='Obisk otrocnice' || visit_type_detail =='Obisk novorojencka'){

        		$('#id_addPatient :selected').each(function(i, selected){
				  patient_num +=1;

				});
				if (patient_num<2){
					alert("Na delovnem nalogu morata biti otročnica in novorojenček");
					return false;
				}

			}else{
        		if(patient_name ==''){
					alert("Ime pacienta je obvezen podatek");
					swal("Napaka", "Ime pacienta je obvezen podatek", "error");
					return false;
				}
			}
	//alert("Before visit count "+visit_count+'; '+time_period+ "empty time interval "+time_interval);
	//casovni interval
	/*if(patient_name ==''){
	    alert("Ime pacienta je obvezen podatek");
	    swal("Napaka", "Ime pacienta je obvezen podatek", "error");
		return false;
	}*/
	if(illness ==''){
	    alert("Bolezen je obvezen podatek");
	    swal("Napaka", "Bolezen je obvezen podatek", "error");
            return false;
	}
	if(visit_count =='' ){
	    alert("Število obiskov je obvezen podatek");
		swal("Napaka", "Število obiskov je obvezen podatek", "error");
            return false;
	}
	if(visit_count > 10 ){
	    alert("Število obiskov ne more biti večje od 10");
		swal("Napaka", "Število obiskov ne more biti večje od 10", "error");
            return false;
	}
	if(time_interval !=''){
		//alert("TIME INTERVAL IS NOT EMPTY");
	    /*if(visit_count<=time_interval){
	    alert("Število obiskov mora biti večje od časovnega intervala");
            return false;
        }*/

    }
    //casovno obdobje
    else{
		//alert("inside time period: ");
		if(time_period !=''){
			if(parseInt(visit_count) > parseInt(time_period)){
				alert("Število obiskov mora biti manjše ali enako števila dni v časovnem obdobju "+ visit_count+'  '+time_period);
				swal("Napaka", "Število obiskov mora biti manjše ali enako števila dni v časovnem obdobju", "error");
					return false;
			}

    	}else{
		alert("Eno izmed polj časovni interval/obdobje mora biti izpolnjeno");
		return false;

    	}


    }
    var medicine_count =0;
    if(visit_type_detail =='Aplikacija injekcij'){


        		$('#id_cureId :selected').each(function(i, selected){
				  medicine_count +=1;
				});

        		if (medicine_count<1){
					alert("Niste izbrali zdravila!");
					return false;
				}

	}

	var material = 0;
	if(visit_type_detail =='Odvzem krvi'){


        		$('#id_materialDN :selected').each(function(i, selected){
				  material += 1;
				});

        		if (material<1){
					alert("Niste izbrali epruvete!");
					return false;
				}

	}

	//$("#confirm").removeAttr('disabled');

	return true;

}
