$(function () {
    //for each in visit_list that is true add it ro id_plan_list


    $("#add_plan").click(function () {
        $("#visit_list > option:selected").each(function () {
            $(this).remove().appendTo("#id_plan_list");
            //rearrangeList("#list2");
        });
    });

    $("#remove_plan").click(function () {
        $("#id_plan_list > option:selected").each(function () {
            $(this).remove().appendTo("#visit_list");
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