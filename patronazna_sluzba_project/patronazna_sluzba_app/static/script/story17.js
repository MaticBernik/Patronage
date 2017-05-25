$(document).ready(function(){

    $('#reset_pass_btn').click(function(e){
    // e.preventDefault();
        var email = $('#reset_mail').val();
        var validation = checkPassword();
        if(!validation){
            e.preventDefault();
        }
        if(email != "undefined" && email != ""){
            //alert("REST PASS "+email);
        }else{
            e.preventDefault();
            sweetAlert("Napaka","Vsi podatki morajo biti izpolnjeni!","error");
        }


    });


});


function checkPassword(){

	var pass1= document.getElementById('reset_password1');
	var pass2 = document.getElementById('reset_password2');
	//store the confirmation message object

	//Set the colors we eill be using
	var goodColor = "#66cc66";
	var badColor = "#ff6666";
   // alert("Inside checkPassword "+pass1.value);
	if(pass1.value.length<8){
		//message.innerHTML = "Geslo mora biti vsaj dolzine 8";
		//window.alert("Geslo mora biti vsaj dolzine 8");
		sweetAlert("Napaka","Geslo mora biti vsaj dolžine 8","error");
		return false;
	}

	if(pass1.value.match(/\d+/g) == null){
		//message.innerHTML = "Geslo mora vsebovati  vsaj eden numericen znak ";
		//window.alert("Geslo mora vsebovati  vsaj eden numericen znak ");
		sweetAlert("Napaka","Geslo mora vsebovati  vsaj eden numericen znak","error");
		return false;
	}
	if(pass1.value == pass2.value){
		return true;
	}else{
		sweetAlert("Napaka","Gesla se ne ujemata!","error");
		return false;
	}
	return true;
}