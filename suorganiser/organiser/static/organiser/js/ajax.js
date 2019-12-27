$(function() {
    var req = $.ajax({
        url: "http://127.0.0.1:8000/sample.json",
        type: "get",
        dataType: "json",
    });
    req.done(function(response, status, jqXHR) {
        console.log(response);
    });
    req.fail(function(jqXHR, status, errorType) {
        console.log(errorType)
    });
});