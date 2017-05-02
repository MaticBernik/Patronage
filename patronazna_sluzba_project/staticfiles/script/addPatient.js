$(document).ready(function() {
  /*  var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
    
    var x = 0; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append('<div><label>Številka kartice otroka</label><input type="number"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
        }
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    });
    */

    //avtomatsko selektiraj prvi element dropdown liste pri podvrsti obiskov

    //gumb za dodajanje novorojencka/pacienta
    $(".add-baby").click(function(e){
        e.preventDefault();
       // alert("dodaj zdravilo search-results "+$("#search").val());
        var patient = $("#searchPatient").val();
        $('#id_addPatient').append('<option value="'+patient+'"'+' selected="true">'+patient+'</option>');
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });

    // gumb za odstranjevanje pacienta
    $(".remove-baby").click(function(e){
        e.preventDefault();
       // alert("Odstranjevanje zdravil");
        $("#id_addPatient > option:selected").each(function(){
            $(this).remove();
        });
        $('#id_addPatient option').prop('selected', true);
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });
    //gumb za dodajanje zdravil pri aplikaciji injekcij
    $(".add-medicine").click(function(e){
        e.preventDefault();
       // alert("dodaj zdravilo search-results "+$("#search").val());
        var medicine = $("#medicine").val();
        $('#id_cureId').append('<option value="'+medicine+'"'+' selected="true">'+medicine+'</option>');
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });

     //gumb za odstranjevanje zdravil pri aplikaciji injekcij
    $(".remove-medicine").click(function(e){
        e.preventDefault();
       // alert("Odstranjevanje zdravil");
        $("#id_cureId > option:selected").each(function(){
            $(this).remove();
        });
         //keep the other selected
        $('#id_cureId option').prop('selected', true);
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });

    //gumb za dodajanje materialov pri odvzemu krvi
    $(".add-material").click(function(e){
        e.preventDefault();

        var testTube = $("#id_materialColor").val();
        var num = $("#stEpruvet").val();
         alert("dodaj material "+testTube+' : '+num);
        $('#id_materialDN').append('<option value="'+testTube+' : '+num+'"'+' selected="true">'+testTube+' : '+num+'</option>');

        //$('#id_materialDN option').prop('selected', true);
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });

    //gumb za odstranjevanje materialov pri odvzemu krvi
    $(".remove-material").click(function(e){
        e.preventDefault();
       // alert("Odstranjevanje zdravil");
        $("#id_materialDN > option:selected").each(function(){
            $(this).remove();
        });
        //keep the other selected
        $('#id_materialDN option').prop('selected', true);
        //$("#search").val().appendTo("#id_cureId");
       // $("#id_cureId").append($("#search").val());

    });

    //modal form preview before submit

    $("#task_preview").click(function(e){
        e.preventDefault();
       //alert("Hello modal form" +$("#visitType").val());
        $("#modal_visit_type").val($("#choose-visit").val());
        $("#modal_visit_detail").val($("#visitType").val());
        $("#modal_patient").val($("#searchPatient").val());
        $("#modal_date").val($("#visitDate").val());

    });

});
