var saved_combat_json = null;

function load_combat() {
    var url = "combat/init/";
    
    $.getJSON( url )
            .done(function( combat_json ) {
                console.log( "Combat JSON loaded");
                initiate_combat_mode(combat_json);
                create_turn_list(combat_json);
                // remember the json data for future reference
                saved_combat_json = combat_json;
                // start turn sequence
                handle_current_turn();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
}

function initiate_combat_mode(combat_json) {
    // display loading div with spinner and "Entering Combat..." 
    $(".loading_spinner").fadeIn(2000);
    // hide script display and all characters (fade out)
    $(".script_display").fadeOut(2000);
    $(".character_panel").fadeOut(2000, function() {

        // update new character position list (still hidden)
        update_character_positions(combat_json.position_list);

        // change background image (during fade out/in so the change isn't too jarring)
        update_background(combat_json.background);

        $(".character_panel").fadeIn(2000, function() {
            // TODO... display empty turn list box
            $(".combat_display").fadeIn("slow", function() {
                $(".loading_spinner").fadeOut("slow");
            });
        });
    });
}

function create_turn_list(combat_json) {
    var position_list = combat_json.position_list;
    var turn_order_list = combat_json.turn_order_list;

    var turn_rows = "";
    for(var index=0; index < turn_order_list.length; index++) {
        position_index = turn_order_list[index];
        character_sheet = position_list[position_index];
        
        var new_row = `
            <tr>
                <td id="turn_${index}"></td><td>${index+1}. ${character_sheet.name}</td>
            </tr>
            `;
        turn_rows += new_row;
    }
    $("#turn_list").html(turn_rows);
}

function handle_current_turn() {
    var url = "combat/turn/";
    
    $.getJSON( url )
            .done(function( turn_json ) {
                console.log( "Turn JSON loaded");
                console.log( "current_turn=" + turn_json.current_turn);
                display_current_turn_arrow(saved_combat_json.turn_order_list, turn_json.current_turn);
                if (turn_json.is_pc == true) {
                    display_combat_frame("combat_action_frame");
                } else {
                    display_combat_frame("combat_narration_frame");
                    // display narration message & wait a few seconds
                    $("#combat_narration_frame_message").html(turn_json.narration);
                    console.log("npc-attack: A");
                    setTimeout(function() {
                        console.log("npc-attack: B");
                        handle_current_turn();
                        console.log("npc-attack: C");
                    }, 5000);
                }
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });

}

function display_current_turn_arrow(turn_order_list, current_turn_index) {
    for(var index=0; index < turn_order_list.length; index++) {
        turn_item_id = "#turn_" + index;
        if (index == current_turn_index) {
            // add arrow in front of current turn's name
            $(turn_item_id).html("<img src=\"/static/images/turn-list-arrow.png\"/>");
        } else {
            // otherwise remove any arrows from the previous turn
            $(turn_item_id).html("");
        }
    }
}

function display_combat_frame(frame_type, display_cancel = false) {
    // hide all frames
    $(".combat_frame").hide();

    // show just the one we're looking for
    if (frame_type == "combat_action_frame") {
        $("#combat_action_frame").show();
    } else if (frame_type == "combat_spell_frame") {
        $("#combat_spell_frame").show();
    } else if (frame_type == "combat_narration_frame") {
        $("#combat_narration_frame").show();
        if (display_cancel == true) {
            $(".cancel_button").show();
        } else {
            $(".cancel_button").hide();
        }
        
    }
}

function handle_attack() {
    display_combat_frame("combat_narration_frame", true);
    $("#combat_narration_frame_message").html("Select a target");
    npc_clicked_action = function(position_index){
        var url = "combat/attack?destination_index=" + position_index;
        $.getJSON( url )
                .done(function( results_json ) {
                    console.log( "Attack JSON loaded");
                    display_combat_frame("combat_narration_frame");
                    // display narration message & wait a few seconds
                    $("#combat_narration_frame_message").html(results_json.narration);
                    console.log("pc-attack: A");
                    setTimeout(function() {
                        console.log("pc-attack: B");
                        handle_current_turn();
                        console.log("pc-attack: C");
                    }, 5000);
                })
                .fail(function( jqxhr, textStatus, error ) {
                    var err = textStatus + ", " + error;
                    console.log( "Request Failed: " + err );
                });
    }
}

function handle_cancel(){
    display_combat_frame("combat_action_frame");
    npc_clicked_action = null;
}