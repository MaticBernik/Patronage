$(document).ready(function() {


    $('#confirm').click(function(e){
        e.preventDefault();
		var work_task_validation = task_validation();
		//alert("Validacija rezultat "+work_task_validation);
        if(!work_task_validation){
			//alert("Insite the if statement");
        	swal("Napaka", "Napaka pri validaciji", "error");
		}else{
        	var form = $(this).parents('form');

        	//zajem vseh podatkov za preview
			var preview_form ='';
        	var visit_type = $("#choose-visit").val();
        	var visit_type_detail = $("#visitType").val();

        	preview_form +='Vrsta obiska: '+visit_type+'\nPodvrsta obiska: '+visit_type_detail+'\nPacient: ';
        	var patient = '';
        	if(visit_type_detail =='Obisk otrocnice in novorojencka' || visit_type_detail =='Obisk novorojencka'){

        		$('#id_addPatient :selected').each(function(i, selected){
				  patient += $(selected).text()+' , ';

				});


			}else{
				patient= $("#searchPatient").val();
			}
			preview_form += patient;

        	var illness = $("#search_illness").val();
        	var visit_date =$("#visitDate").val();
        	var mandatory = $("#id_mandatory").val();
        	var visit_count =$("#id_visitCount").val();
        	var time_interval = $("#timeInterval").val();

        	if(mandatory =='on'){
				mandatory = 'Obvezen';
			}else{
				mandatory = 'Okviren';
			}


        	if(time_interval !=''){
				var temp_period = time_interval * visit_count;
        		preview_form +='\nBolezen: '+illness+'\nPrvi obisk: '+visit_date+'\nObvezen: '+mandatory+'\nStevilo obiskov: '+visit_count+
					'\nČasovni interval: '+time_interval+"\nČasovno obdobje: "+temp_period;
			}else{

				var time_period = $("#timePeriod").val();
				var temp_interval = time_period/visit_count;
        		preview_form +='\nBolezen: '+illness+'\nPrvi obisk: '+visit_date+'\nObvezen: '+mandatory+'\nStevilo obiskov: '+visit_count+
					'\nČasovni interval: '+temp_interval+'\nČasovno obdobje: '+time_period;
			}




        	if(visit_type_detail =='Aplikacija injekcij'){
				var medicine = '\nZdravila: ';

        		$('#id_cureId :selected').each(function(i, selected){
				  medicine += $(selected).text()+' , ';
				});
        		preview_form += medicine;
			}


        	if(visit_type_detail =='Odvzem krvi'){
				var material = '\nEpruvete: ';

        		$('#id_materialDN :selected').each(function(i, selected){
				  material += $(selected).text()+' , ';
				});
        		preview_form += material;
			}
			preview_form +='\n';
				swal({
				  title: "Potrditev podatkov",
				  text: preview_form,
				  type: "warning",
				  showCancelButton: true,
				  confirmButtonColor: "#3add86",
				  confirmButtonText: "Da, Potrdi",
				  cancelButtonText: "Ne, Zavrni",
				  closeOnConfirm: false,
				  closeOnCancel: true
				},
				function(isConfirm){
				  if (isConfirm) {
					  form.submit();
				   // swal("Deleted!", "Your imaginary file has been deleted.", "success");
				  } else {
					swal("Cancelled", "Your imaginary file is safe :)", "error");
				  }
				});
			   //alert("Hello modal form" +$("#visitType").val());
			   /* $("#modal_visit_type").val($("#choose-visit").val());
				$("#modal_visit_detail").val($("#visitType").val());
				$("#modal_patient").val($("#searchPatient").val());
				$("#modal_date").val($("#visitDate").val());
		*/


		}
	});

	//VALIDACIJA PRI REGISTRACIJI PACIENTA/OSKRBOVANCA
    $(".signupbtn").click(function(){
		//alert("hello world");
		var birthResult = false;
		try{
			birthResult = birthDate();
		}catch (e){
			//alert("Error birthResult");
		}

		//alert("Hello again!!!");
		//alert("Rezultat birthResult: "+ birthResult);
		
		
		var inputResult = registrationValidation();
		//alert("Rezultat regValidat: "+inputResult);
		inputResult = inputResult && birthResult;
		//alert("Rezultat AND: "+inputResult);
		
		if(!inputResult){
				$("form").submit(function(e){
					//alert('inputResult is false');
                e.preventDefault(e);
				$(this).unbind(e);
            });
			}
		//alert("this query works");
		
		//alert("Rezultat validacije main "+inputResult);
		//check contact fields
		var cName = document.getElementById("contact_first_name");
		var cSurname = document.getElementById("contact_last_name");
		var cAddress = document.getElementById("contact_address");
		var cPhoneNumber = document.getElementById("contact_phone_number");
		var bloodRelation = document.getElementById("contact_sorodstvo");
		//var test = true;
		//alert("test "+test+" input: "+inputResult);
		//console.log("test "+test+" input: "+inputResult);
		
		//alert("Contakt surname value: "+cSurname.value);
		
		if((cName.value == "" && cSurname.value == "" && cAddress.value == "" && cPhoneNumber.value == ""
		&& bloodRelation.value == "")){
			//the field are empty
			
		}else if ((cName.value != "" && cSurname.value != "" && cAddress.value != "" && cPhoneNumber.value != ""&& bloodRelation.value != "")){
			//do contact validation
			//alert("Contact validation");
			var uC = "[A-Z\u010C\u0160\u017d\u0106\u0110]";
			var lC="[a-z\u010d\u0161\u017e\u0107\u0111]";
			var allCase = "[A-Z\u010C\u0160\u017d\u0106\u0110\a-z\u010d\u0161\u017e\u0107\u0111]";
			var badColor = "#ff6666";
			//var nameRE = new RegExp("^("+uC+lC+"+)");
			//lowerCase
			var nameRE = new RegExp("^("+allCase+"+)");
			//did the validation pass
			
			
			if(cSurname.value.match(nameRE)== null){
				alert("Napacen vnos priimka kontakt");
				cSurname.style.backgroundColor = badColor;
				inputResult = false;
				console.log(cSurname);
			}else if(cName.value.match(nameRE) == null){
				alert("Napacen vnos imena kontakt");
				cName.style.backgroundColor = badColor;
				inputResult=false;
			}else if(cPhoneNumber.value.length<9){
				alert("Napacen vnos telefonske stevilke kontakt");
				cPhoneNumber.style.backgroundColor = badColor;
				inputResult = false;
			}
			//alert("Dodatni "+phone.value.length+" input: "+inputResult);
		}else{
			//alert("Za kontaktno osebo morajo biti izpolnjeni vsi podatki ali pa nobeden ");
			
			$("form").submit(function(e){
                alert('Za kontaktno osebo morajo biti izpolnjeni vsi podatki ali pa nobeden!');
                e.preventDefault(e);
				$(this).unbind(e);
            });
		}
		
		if(!inputResult){
				$("form").submit(function(e){
					//alert('inputResult is false');
                e.preventDefault(e);
				$(this).unbind(e);
            });
			}
	});
});
var modal;

/*hide the div with extra contact data*/

$(document).ready(function(){
	$("#myDIV").hide();
}

);
function myFunction() {
    var x = document.getElementById('myDIV');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}

function showModal(){
	var x = document.getElementById("id01").style.display='block';
	modal = document.getElementById('id01');
}

function cancelModal(){
	document.getElementById('id01').style.display='none';
}

	// Get the modal
//var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function checkPassword(){
	
	var pass1= document.getElementById('pass1');
	var pass2 = document.getElementById('pass2');
	//store the confirmation message object
	var message = document.getElementById('confirmMessage');
	//Set the colors we eill be using
	var goodColor = "#66cc66";
	var badColor = "#ff6666";
	//Compare the values in the password field and the confirmation filed
	if(pass1.value.length<8){
		//message.innerHTML = "Geslo mora biti vsaj dolzine 8";
		window.alert("Geslo mora biti vsaj dolzine 8");
		return false;
	}
	if(pass1.value.match(/\d+/g) == null){
		//message.innerHTML = "Geslo mora vsebovati  vsaj eden numericen znak ";
		window.alert("Geslo mora vsebovati  vsaj eden numericen znak ");
		return false;
	}
	if(pass1.value == pass2.value){
		pass2.style.backgroundColor = goodColor;
		/*message.style.color = goodColor;
		message.innerHTML = pass1.value;*/
		return true;
	}else{
		pass2.style.backgroundColor= badColor;
		window.alert("Gesla se ne ujemata!");
		/*message.style.color = badColor;
		message.innerHTML = pass1.value;*/
		return false;
	}
	return true;
}

function firstVisitDate(){
	var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();
	
	var datum = document.getElementById('visitDate');
	var message = document.getElementById('message');
	
	var firstVisit = datum.value.split(".");
	//alert("today:"+firstVisit[2]);
	if(firstVisit[2]<year1){
		alert("Napacno leto! Datum ne more biti v preteklosti");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	if(firstVisit[2]==year1 && firstVisit[1]<month1){
		alert("Napacen datum! Datum obiska mora biti vecji od trenutnega!");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	if(firstVisit[2] == year1 && firstVisit[1] == month1 && firstVisit[0] <= day1){
		alert("Napacen datum! Datum obiska mora biti vecji od trenutnega!");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}

	//preveri se dodatna polja
	//if($(''))
	$(".signupbtn").removeAttr('disabled');
	return true;
	/*var currentDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
	var chosenDate = Date.parse(datum.value);
	message.innerHTML ='today:' +currentDate+' , chosen: '+datum.value;*/
}

function birthDate(){
	var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();
	
	var datum = document.getElementById('birth_date');
	var message = document.getElementById('message');
	if(datum.value ==''){
		alert("Napačen datum");
		return false;
	}
	
	var birth = datum.value.split(".");
	//alert("datum rojstva primerjava: "+birth[0]+' : '+day1);
	//alert("today:"+firstVisit[2]);
	if(birth[2]>year1){
		alert("Napacna letnica rojstva");
		//$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	if(birth[2]==year1 && birth[1]>month1){
		alert("Napacen datum! Datum rojstva mora biti manjsi od trenutnega! Napacen mesec!");
		//$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	if(birth[2] == year1 && birth[1] == month1 && birth[0] > day1){
		alert("Napacen datum! Datum obiska mora biti manjsi od trenutnega! Napacen dan!");
		//$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	return true;
	/*var currentDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
	var chosenDate = Date.parse(datum.value);
	message.innerHTML ='today:' +currentDate+' , chosen: '+datum.value;*/
	
}

function addPatientButton(){
	
	var s = document.getElementById("visitType").value;
	//alert(s);
	if((s == "Obisk otrocnice in novorojencka" )|| (s== "Obisk novorojencka")){

		document.getElementById("cureId").style.display = 'none';
		document.getElementById('materialId').style.display = 'none';
		/*alert("Before mumbo jumbo");
		document.getElementsByClassName("add-baby").style.display='block';
		document.getElementById("baby-patient").style.display ='block';
		document.getElementsByClassName("remove-baby").style.display='block';*/
		//alert("BEFORE Make required");
		//make required
		document.getElementById("id_addPatient").required = true;
		//remove required
		document.getElementById("id_cureId").removeAttribute("required");
		document.getElementById("id_materialDN").removeAttribute("required");
	}else if(s == 'Aplikacija injekcij'){
		//alert("changed to injection");
		document.getElementById("cureId").style.display = 'block';

		//make required
		document.getElementById("id_cureId").required = true;
		//remove required
		document.getElementById("id_addPatient").removeAttribute("required");
		document.getElementById("id_materialDN").removeAttribute("required");

		//hide this
		document.getElementById('materialId').style.display = 'none';
	}else if (s == 'Odvzem krvi'){
		document.getElementById('materialId').style.display = 'block';
		//make required
		document.getElementById("id_materialDN").required = true;
		//remove required
		document.getElementById("id_cureId").removeAttribute("required");
		document.getElementById("id_addPatient").removeAttribute("required");
		//hide this
		document.getElementById("cureId").style.display = 'none';
	}
	else{
		//document.getElementById("message").innerHTML = this.options[this.selectedIndex].innerHTML;
		$(".add-baby").attr('disabled','disabled');
		$(".add-baby").hide();
		$(".remove-baby").attr('disabled','disabled');
		$(".remove-baby").hide();
		$("#baby-patient").hide();
		$("#materialId").hide();
		$("#cureId").hide();
		//remove required
		document.getElementById("id_cureId").removeAttribute("required");
		document.getElementById("id_addPatient").removeAttribute("required");
		document.getElementById("id_materialDN").removeAttribute("required");

	}
}

$(document).ready(function() {

	$("#choose-visit").change(function(){
		//alert($("#visitType").find("option:first-child").val());

		$(".add-baby").attr('disabled','disabled');
		$(".add-baby").hide();
		$(".remove-baby").attr('disabled','disabled');
		$(".remove-baby").hide();
		$("#baby-patient").hide();
		$("#materialId").hide();
		$("#cureId").hide();
	});

	$("#visitType").change(function() {
		if($("#visitType option:selected").text() == "Obisk otrocnice in novorojencka"||$("#visitType option:selected").text() == "Obisk novorojencka" ){
			$(".add-baby").show();
			$(".add-baby").removeAttr('disabled');

			$(".remove-baby").show();
			$(".remove-baby").removeAttr('disabled');
			$("#baby-patient").show();
			$("#baby-patient").prop('required',true);

		}else{
			$(".add-baby").attr('disabled','disabled');
			$(".add-baby").hide();
			$(".remove-baby").attr('disabled','disabled');
			$(".remove-baby").hide();
			$("#baby-patient").hide();
		}
		
});
	$("#timeInterval").on('input',function(){
		$("#timePeriod").attr('disabled','disabled');
	});
	
	$("#timePeriod").on('input',function(){
		$("#timeInterval").attr('disabled','disabled');
	});
	
	$("#timeInterval").on('focusout',function(){
		if($("#timeInterval").val() == "" ){
			$("#timePeriod").removeAttr('disabled');
		}
		
	});
	
	
	$("#timePeriod").on('focusout',function(){
		if($("#timePeriod").val() == "" ){
			$("#timeInterval").removeAttr('disabled');
		}
		
	});
	
});


// preveri vnos uporabnika
function registrationValidation(){
	
	var uC = "[A-Z\u010C\u0160\u017d\u0106\u0110]";
	var lC="[a-z\u010d\u0161\u017e\u0107\u0111]";
	var allCase = "[A-Z\u010C\u0160\u017d\u0106\u0110\a-z\u010d\u0161\u017e\u0107\u0111]";
	var badColor = "#ff6666";
	//ime in priimek morajo biti z veliko zacetnico
	//var nameRE = new RegExp("^("+uC+lC+"+)");
	//lowerCase
	var nameRE = new RegExp("^("+allCase+"+)");
	var name= document.getElementById('first_name');
	var surname = document.getElementById('last_name');
	var cardNumber = document.getElementById('card_number');
	var phone = document.getElementById('phone');

	//alert("Vneseno ime: "+name.value+" priimek: "+surname.value);
	//var birthDate = document.getElementById('birthDate');
	//var address = document.getElementById('address');
	//console.log(name.value+", reges: "+name.value.match(nameRE));
	//alert('Before passwordCheck ');
	//var passCheck = checkPassword();
	//alert('Rezultat passworda: '+passCheck);
	if(cardNumber.value.length != 12){
		alert("Dolzina stevilke Zdravstvene kartice mora biti 12");
		cardNumber.style.backgroundColor = badColor;
		return false;
	}else if(surname.value.match(nameRE) == null){
		alert("Napacen vnos priimka");
		surname.style.backgroundColor = badColor;
		return false;
	}else if(name.value.match(nameRE) == null){
		alert("Napacen vnos imena");
		name.style.backgroundColor = badColor;
		return false;
	}else if(phone.value.length<9){
		alert("Napacen vnos telefonske stevilke");
		phone.style.backgroundColor = badColor;
		return false;
	}
	
	try{
		//alert('try happend');
		return checkPassword();
	}catch(err){
		//alert('err');
		return true;
	}
}
