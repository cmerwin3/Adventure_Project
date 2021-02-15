    
    
function update_character_positions(script_json) {
    var new_row = "";
    for(var index=0; index<=3; index++) {
        character_sheet = script_json.position_list[index];
        
        // create new character <td> html element string and plug in the values
        var new_elem = `
            <td class="character" id="char_${character_sheet.id}">
                <img src="/static/images/character-${character_sheet.avatar_id}.png"/><br/>
                ${character_sheet.name}
                <div class="character-tooltip">
                    Class: ${character_sheet.class_level.class_type}<br/>
                    Level: ${character_sheet.class_level.level}<br/>
                    Strength: ${character_sheet.strength}<br/>
                    Dexterity: ${character_sheet.dexterity}<br/>
                    Constitution: ${character_sheet.constitution}<br/>
                    Intelligence: ${character_sheet.intelligence}<br/>
                    Wisdom: ${character_sheet.wisdom}<br/>
                    Charisma: ${character_sheet.charisma}<br/>
                    Hit Points: ${character_sheet.hit_points_current} / ${character_sheet.hit_points_total}<br/>
                </div>
            </td>
            `;
        new_row += new_elem;
    }
    $("#pc_character_row").html(new_row);

    new_row = "";
    for(var index=4; index < script_json.position_list.length; index++) {
        character_sheet = script_json.position_list[index];
        
        // create new character <td> html element string and plug in the values
        var new_elem = `
            <td class="character" id="char_${character_sheet.id}">
                <img src="/static/images/npc-${character_sheet.avatar_id}.png"/><br/>
                ${character_sheet.name}
            </td>
            `;
        new_row += new_elem;
    }
    $("#npc_character_row").html(new_row);

}
    
    

function display_character_health() {
    var hit_points_total = character_list[0].hit_points_total;
    var hit_points_current = character_list[0].hit_points_current;
    var percentage = (hit_points_current/hit_points_total)*100;

    var character_element = $(".character")[0];

    var color;
    var opacity = "1";
    if (percentage == 100) {
        color="green";
    } else if (percentage > 50) {
        color="yellow";
    } else if (percentage > 0) {
        color="red";
    } else {
        color="grey";
        opacity=".7";
    }
    character_element.style["border-color"]=color;
    character_element.style["opacity"]=opacity;
}

function initiate_combat_mode() {
    // hide script display and all characters (fade out)
    $(".script_display").fadeOut(2000);
    $(".character").fadeOut(2000);

    // display loading div with spinner and "Entering Combat..." 
    $(".loading_spinner").fadeIn(2000, function() {
        // change background image (fade out/in so the change isn't too jarring)
        $(".character_panel").delay(2000).fadeOut("fast", function() {
            $(".character_panel").css("background-image", "url('/static/images/background_combat.jpg')");
            $(".character_panel").fadeIn("fast", function() {
                // display empty turn list box
                $(".combat_display").delay(2000).fadeIn("slow", function() {
                    // add in new characters sequentially to turn list and character panel
                    $(".character").delay(2000).fadeIn(2000, function() {
                        $(".loading_spinner").fadeOut("fast");
                    });
                });
            });
        });
    });


    // hide script display and all characters (fade out)
    //$(".script_display").fadeOut(2000);
    //$(".character").fadeOut(2000);

    // display spinner with "Entering Combat..." on color display div
    //$(".color_display").show();
    //$(".loading_spinner").fadeIn();

    // change background image
    //$(".character_panel").css("background-image", "url('/static/images/background_combat.jpg')");

    // display empty turn list box
    //$(".combat_display").fadeIn("slow");

    // add in new characters sequentially to turn list and character panel

    // remove spinner

    // send server 'ready for combat' and reponse will be first turn 

}


