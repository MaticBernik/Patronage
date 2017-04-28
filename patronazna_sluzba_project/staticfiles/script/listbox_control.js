$(function () {
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
});