$(document).ready(function() {
 // executes when HTML-Document is loaded and DOM is ready
// alert("document is ready");
    $("input").addClass("form-control" );
    $("select").addClass("form-control");
    $("label").addClass("control-label");
    $("in_wrap").addClass("col-lg-10 col-lg-offset-1  col-md-8 col-md-offset-2 col-sm-8 col-sm-offset-2 col-xs-10 col-xs-offset-1");
    $("#id_mandatory").removeClass("form-control");
});