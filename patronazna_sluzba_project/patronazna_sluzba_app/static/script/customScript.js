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
	
}

function firstVisitDate(){
	var today = new Date();
	var day1 = today.getDate();
	var month1 = (today.getMonth()+1);
	var year1 = today.getFullYear();
	
	var datum = document.getElementById('visitDate');
	var message = document.getElementById('message');
	
	var firstVisit = datum.value.split("-");
	
	if(firstVisit[0]<year1){
		alert("Napacno letnico");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	if(firstVisit[0]==year1 && firstVisit[1]<month1){
		alert("Napacen datum");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	if(firstVisit[0] == year1 && firstVisit[1] == month1 && firstVisit[2] < day1){
		alert("Napacen datum");
		$(".signupbtn").attr('disabled','disabled');
		return false;
	}
	
	$(".signupbtn").removeAttr('disabled');
	
	var currentDate = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
	var chosenDate = Date.parse(datum.value);
	message.innerHTML ='today:' +currentDate+' , chosen: '+datum.value;
}

function addPatientButton(){
	
	var s = document.getElementById("visitType").value;
	if(s.value == "Obisk otročnice in novorojenčka"){
		document.getElementByClassName("add_field_button").style.display='block';
	}else{
		document.getElementById("message").innerHTML = this.options[this.selectedIndex].innerHTML;
	}
}

$(document).ready(function() {
	$("#visitType").change(function() {
		if($("#visitType option:selected").text() == "Obisk otročnice in novorojenčka"){
			$(".add_field_button").show();
			$(".add_field_button").removeAttr('disabled');
		}else{
			$(".add_field_button").attr('disabled','disabled');
		}
		
});
	$("#timeInterval").on('input',function(){
		$("#timeSpan").attr('disabled','disabled');
	});
	
	$("#timeSpan").on('input',function(){
		$("#timeInterval").attr('disabled','disabled');
	});
	
	$("#timeInterval").on('focusout',function(){
		if($("#timeInterval").val() == "" ){
			$("#timeSpan").removeAttr('disabled');
		}
		
	});
	
	
	$("#timeSpan").on('focusout',function(){
		if($("#timeSpan").val() == "" ){
			$("#timeInterval").removeAttr('disabled');
		}
		
	});
	
	
	
	$(".signupbtn").click(function(){
		//check contact fields
		var cName = $("#contact_name").val();
		var cSurname = $("#contact_surname").val();
		var cAddress = $("#contact_address").val();
		var cPhoneNumber = $("#contact_phone_number").val();
		var bloodRelation = $("#sorodstvo").val();
		
		if((cName == "" && cSurname == "" && cAddress == "" && cPhoneNumber == ""
		&& bloodRelation == "") || (cName != "" && cSurname != "" && cAddress != "" && cPhoneNumber != ""&& bloodRelation != "")){
			continue;
		}else{
			//alert("Za kontaktno osebo morajo biti izpolnjeni vsi podatki ali pa nobeden ");
			
			$("form").submit(function(e){
                alert('submit intercepted');
                e.preventDefault(e);
            });
		}
	});
});




