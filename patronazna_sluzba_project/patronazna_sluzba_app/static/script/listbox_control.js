$(function () {
    //for each in visit_list that is true add it ro id_plan_list


    $("#add_plan").click(function () {
        $("#visit_list > option:selected").each(function () {
            $(this).remove().appendTo("#id_plan_list");
            //rearrangeList("#list2");
        });
    });

    $("#remove_plan").click(function (e) {
        $("#id_plan_list > option:selected").each(function () {
           // alert("Odstrani izbrano opcijo");
            //alert("Opcija: "+$(this).text().indexOf('Obvezen'));
            if(($(this).text().indexOf('Obvezen'))>-1){
                alert("Datum obiska je obvezen");
                e.preventDefault();
            }else{
                $(this).remove().appendTo("#visit_list");
            }

            //rearrangeList("#list1");
        });
    });

   /* alert("document is ready");
    $("#visit_list > option").each(function () {
        var plan_data = $(this).text();
        alert("This is data: "+plan_data);
           // $(this).remove().appendTo("#id_plan_list");
            //rearrangeList("#list2");
        });*/
});