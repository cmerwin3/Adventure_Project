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
    $(".loading_spinner").fadeIn("slow");
    $("#spinner_text").text("Entering Combat");
    // hide script display and all characters (fade out)
    $(".script_display").fadeOut("slow");
    $(".character_panel").fadeOut("slow", function() {

        // update new character position list (still hidden)
        update_character_positions(combat_json.position_list);

        display_character_health(combat_json.position_list);

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

function end_combat_mode(script_id) {
    // display loading div with spinner and "Entering Combat..." 
    $(".loading_spinner").fadeIn("slow");
    $("#spinner_text").text("Exiting Combat");
    // hide script display and all characters (fade out)
    $(".combat_display").fadeOut("slow");
    $(".character_panel").fadeOut("slow", function() {
        callback = function() {
            $(".character_panel").fadeIn(2000, function() {
                $(".script_display").fadeIn("slow", function() {
                    $(".loading_spinner").fadeOut("slow");
                });
            });
        }
        load_script(script_id, callback);
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
            .done(function(turn_json) {
                console.log("Turn JSON loaded");
                console.log("current_turn=" + turn_json.current_turn);
                display_current_turn_arrow(saved_combat_json.turn_order_list, turn_json.current_turn);
                
                if (turn_json.turn_status == "end_combat") {
                    display_combat_frame("combat_narration_frame", false, narration_text = turn_json.end_combat_data.narration);
                    refresh_position_list();
                    setTimeout(function() {
                        end_combat_mode(turn_json.end_combat_data.next_script);
                    }, 5000);
                } else if (turn_json.turn_status == "skip_turn") {
                    display_combat_frame("combat_narration_frame", false, narration_text = turn_json.skip_turn_data.narration);
                    refresh_position_list();
                    setTimeout(function() {
                        handle_current_turn();
                    }, 5000);
                } else if(turn_json.turn_status == "pc_turn") {
                    display_combat_frame("combat_action_frame");
                } else if (turn_json.turn_status == "npc_turn") {
                    display_attack_results(turn_json.npc_turn_data)
                }
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });

}

function refresh_position_list(callback = null){
    console.log("before refresh");

    
    var url = "combat/positions/";
    $.getJSON( url )
            .done(function( position_list_json ) {
                console.log( "Positions JSON loaded");
                saved_combat_json.position_list = position_list_json.position_list;
                update_character_positions(saved_combat_json.position_list);
                display_character_health(saved_combat_json.position_list);
                console.log("after refresh");


                if (callback != null) {
                    callback();
                }
                //$("#character_panel").trigger("refreshed");
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            })
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

function display_combat_frame(frame_type, display_cancel = false, narration_text = null) {
    // hide all frames
    $(".combat_frame").hide();

    // show just the one we're looking for
    if (frame_type == "combat_action_frame") {
        $("#combat_action_frame").show();
    } else if (frame_type == "combat_spell_frame") {
        $("#combat_spell_frame").show();
    } else if (frame_type == "combat_narration_frame") {
        
        $("#combat_narration_frame").show();
        if (narration_text != null) {
            $("#combat_narration_frame_message").hide();
            $("#combat_narration_frame_message").html(narration_text);
            $("#combat_narration_frame_message").fadeIn("fast");
        }
        if (display_cancel == true) {
            $(".cancel_button").show();
        } else {
            $(".cancel_button").hide();
        }
        
    }
}

function handle_attack() {
    display_combat_frame("combat_narration_frame", true, narration_text = "Select a target");
    //$("#combat_narration_frame_message").html("Select a target");
    //$("#char_1").style["border-color"]="white";
    //$("#char_1").css("border-color", "red");

    highlight_npc_characters(saved_combat_json.position_list);
    npc_clicked_action = function(position_index){
        display_character_health(saved_combat_json.position_list);
        highlight_npc_characters(saved_combat_json.position_list, position_index);
        var url = "combat/attack?destination_index=" + position_index;
        $.getJSON( url )
                .done(function(results_json) {
                    console.log("Attack JSON loaded");
                    display_attack_results(results_json)
                })
                .fail(function( jqxhr, textStatus, error ) {
                    var err = textStatus + ", " + error;
                    console.log( "Request Failed: " + err );
                });
    }
}

function display_attack_results(attack_results_data) {
    display_combat_frame("combat_narration_frame", false, narration_text = attack_results_data.narration);
    //$("#character_panel").on("refreshed", function(){
    var callback = function(){
        destination_index = attack_results_data.destination_ids[0];
        damage = attack_results_data.damage;
        animate_character_damage(destination_index, damage);
        setTimeout(function() {
            handle_current_turn();
        }, 5000); 
    } ;
    refresh_position_list(callback);
    
}

function handle_cancel(){
    display_combat_frame("combat_action_frame");
    npc_clicked_action = null
}

function animate_character_damage(destination_index, damage) {
    console.log("destination_index=" + destination_index);
  
    // determine the character td cell and overlay to be animated
    td_elem = $("#char_" + destination_index);
    overlay_elem = $("#char_overlay_" + destination_index);
   
    // display the damage in the overlay
    damage_str = "miss"; 
    if (damage > 0) {
        damage_str = "-" + damage;
    }
    overlay_elem.html(damage_str);
  
    // start shake animation, see js library docs at https://animate.style
    console.log("before animation");

    td_elem.addClass( "animate__animated animate__tada" );
    td_elem.on("animationend", function(){
        // when animation is complete, remove animation classes and clear damage overlay
        td_elem.removeClass( "animate__animated animate__tada" );
        overlay_elem.html("");
        console.log("after animation");
    })
 }
 
