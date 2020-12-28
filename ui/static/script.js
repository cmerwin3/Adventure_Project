
function load_script(script_id) {
   var url = "script/" + script_id;

   $.getJSON( url )
            .done(function( json ) {
                console.log( "Script JSON loaded: " + json.id );
                $("#prompt").text(json.prompt);
            })

            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
}


