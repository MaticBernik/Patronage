
function task_validation(){
    //alert("Hello this is task validator");
	var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();

	var datum = document.getElementById('visitDate');
	var message = document.getElementById('message');

	var firstVisit = datum.value.split(".");
	//alert("today:"+firstVisit[2]);
	if(firstVisit[2]<year1){
		alert("Napacno letnico");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	if(firstVisit[2]==year1 && firstVisit[1]<month1){
		alert("Napacen datum! Datum obiska mora biti vecji ali enak trenutnega!");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}

	if(firstVisit[2] == year1 && firstVisit[1] == month1 && firstVisit[0] < day1){
		alert("Napacen datum! Datum obiska mora biti vecji ali enak trenutnega!");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}

	var visit_count  = document.getElementById('id_visitCount').value;
	var time_interval = document.getElementById('timeInterval').value;
	var time_period = document.getElementById('timePeriod').value;
	//casovni interval
	if(time_interval !=''){
	    if(visit_count<=time_interval){
	    alert("Število obiskov mora biti večje od časovnega intervala")
            return false;
        }
    }
    //casovno obdobje
    else{
	    if(visit_count>=time_period){
	    alert("Število obiskov mora biti manjše od časovnega obdobja")
            return false;
        }

    }

	$(".signupbtn").removeAttr('disabled');
	return true;
	/*var currentDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
	var chosenDate = Date.parse(datum.value);
	message.innerHTML ='today:' +currentDate+' , chosen: '+datum.value;*/
}
