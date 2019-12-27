/*
$(function() {
    
    var test = $.ajax({
        "url": "http://127.0.0.1:8000/sample.json",
        "type": "get",
        "dataType": "json",
    }).done(function(results, status, jqXHR) {
        console.log(results);
        }).fail(function(jqXHR, status, errorThrown) {
            console.log("fail", arguments);
            }).always(function() {
                console.log(`me: `, arguments)
                });

    var req = $.getJSON(
        "http://127.0.0.1:8000/sample.json",
        function(data) {
            console.log(data, arguments);
        }
    )
    req.done(function() {
        console.log("datpiff");
        console.log(req);
    })
    

    // $.ajax({
    //     "url": "http://amazon.com",
    //     "type": "get",
    //     "datatype": "json"
    // }).done(function(response) {
    //     console.log(response);
    //     });
});
*/