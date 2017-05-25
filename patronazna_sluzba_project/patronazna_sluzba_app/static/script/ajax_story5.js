    // ajax za obisk glede na role
$(document).ready(function(){

//alert("VISIT ROLE GET REQUEST");
     $.ajax({

            type: "GET",
            url: "/visit/role/",
            data: {
                'choose_visit': $('#choose-visit').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },

            success: chooseRoleSuccess,
            dataType: 'html'
        });

});

function chooseRoleSuccess(data, textStatus, jqXHR) {
    $('#choose-visit').html(data);
}