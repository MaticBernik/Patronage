$(document).ready(function() {
	
    $(".signupbtn").click(function(){
		//alert("hello world");
		var birthResult = birthDate();
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
		var cName = document.getElementById("contact_name");
		var cSurname = document.getElementById("contact_surname");
		var cAddress = document.getElementById("contact_address");
		var cPhoneNumber = document.getElementById("contact_phone_number");
		var bloodRelation = document.getElementById("relation");
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
	var passw = document.getElementById('pass2');
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
		alert("Napacen datum! Datum obiska mora biti vecji ali enak trenutnega!");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	if(firstVisit[2] == year1 && firstVisit[1] == month1 && firstVisit[0] < day1){
		alert("Napacen datum! Datum obiska mora biti vecji ali enak trenutnega!");
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
	
	var datum = document.getElementById('birthDate');
	var message = document.getElementById('message');
	
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
	if((s == "Obisk otrocnice" )|| (s== "Obisk novorojencka")){
		//alert("changed to prevention");
		//hide these fields
		document.getElementById("cureId").style.display = 'none';
		document.getElementById('materialId').style.display = 'none';
		
		document.getElementsByClassName("add-baby").style.display='block';
		document.getElementById("baby-patient").style.display ='block';
		document.getElementsByClassName("remove-baby").style.display='block';

		//make required
		document.getElementById("id_addPatient").required = true;
		//remove required
		document.getElementById("id_cureId").required = false;
		document.getElementById("id_materialDN").required = false;
	}else if(s == 'Aplikacija injekcij'){
		//alert("changed to injection");
		document.getElementById("cureId").style.display = 'block';

		//make required
		document.getElementById("id_cureId").required = true;
		//remove required
		document.getElementById("id_addPatient").required = false;
		document.getElementById("id_materialDN").required = false;

		//hide this
		document.getElementById('materialId').style.display = 'none';
	}else if (s == 'Odvzem krvi'){
		document.getElementById('materialId').style.display = 'block';
		//make required
		document.getElementById("id_materialDN").required = true;
		//remove required
		document.getElementById("id_cureId").required = false;
		document.getElementById("id_addPatient").required = false;
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
		if($("#visitType option:selected").text() == "Obisk otrocnice"||$("#visitType option:selected").text() == "Obisk novorojencka" ){
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
	var name= document.getElementById('name');
	var surname = document.getElementById('surname');
	var cardNumber = document.getElementById('cardNumber');
	var phone = document.getElementById('phone');
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
	}else if(surname.value.match(nameRE)== null){
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
