

$(document).ready(function() {
    load_script();
});

var current_script_id = null;


function load_script(script_id) {
    if (script_id == null)
        script_id = "";

    var url = "script/" + script_id;
    
    $.getJSON( url )
            .done(function( script_json ) {
                console.log( "Script JSON loaded: " + script_json.script_id );
                current_script_id = script_json.script_id
                //TODO Naming convention to 'Panel_Component'
                update_background(script_json);
                update_dialogue_panel(script_json);
                update_character_positions(script_json);
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
}

function update_background(script_json) {
    var image_url = "/static/images/" + script_json.background;
    $("div.character_panel").css("background-image", "url('" + image_url + "')");
}

function update_dialogue_panel(script_json) {
    // replace prompt 
    $("#prompt").text(script_json.prompt);
    
    // replace each response
    var index = 0;
    for (; index < script_json.responses.length; index++) {
        // determine button char to show based on index (e.g. index 2 shows as 'C')
        var button_char = String.fromCharCode('A'.charCodeAt(0) + index);

        var new_td = `
            <button onclick="handle_response(${index})">${button_char}</button>
            ${script_json.responses[index].response}
            `;
        $("#response_" + index).html(new_td);
    }

    // if less than 6 responses, clear out any previous response items
    for (; index <= 5; index++) {
        $("#response_" + index).html("");
    }
}




/**
 * 
 * Called when the user clicks a response button in the dialogue panel
 * 
 * @param {*} response_id 
 */
function handle_response(response_id) {
    var url = "script/" + current_script_id + "/" + response_id;
    $.getJSON( url )
            .done(function( response_json ) {
                console.log( "Response JSON loaded: " + response_json );
                if (response_json.next_script != null) {
                    load_script(response_json.next_script)
                }
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    
    
    
    
    // TODO - call rest api to tell server what response was selected
    //      - based on the server's json response:
    //          A) start combat mode  
}

