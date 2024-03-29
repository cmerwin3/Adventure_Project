//This javascript handles the dynamic functionalites of moving from one script to the next.


// at home page startup load the default script
$(document).ready(function() {
    load_script();
});

var current_script_id = null;

/**
 * 
 * Load a script (prompt, responses, npc's, etc) into the home page
 * 
 * @param {string} script_id The specific script_id to load, if unspecified let server decide default 
 */
function load_script(script_id, callback = null) {
    if (script_id == null)
        script_id = "";

    var url = "script/" + script_id;
    
    $.getJSON( url )
            .done(function( script_json ) {
                console.log( "Script JSON loaded: " + script_json.script_id );
                current_script_id = script_json.script_id
                update_background(script_json.background);
                update_dialogue_panel(script_json);
                update_character_positions(script_json.position_list);
                if (callback != null) {
                    callback();
                }
             })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
}


function update_background(background) {
    var image_url = "/static/images/" + background;
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
 * @param {int} response_id index for the response (0-based: 'A'=0, 'B'=1, etc.)
 */
function handle_response(response_id) {
    var url = "script/" + current_script_id + "/" + response_id;
    $.getJSON( url )
            .done(function( response_json ) {
                console.log( "Response JSON loaded: " + response_json );
                if (response_json.combat_mode != null) {
                    load_combat();
                }
                else if (response_json.next_script != null) {
                    load_script(response_json.next_script);
                }
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
}

