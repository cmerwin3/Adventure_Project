    
// calback funtion for when an NPC is Clicked
var npc_clicked_action = null



function update_character_positions(position_list) {
    var new_row = "";
    for(var index=0; index<=3; index++) {
        character_sheet = position_list[index];
        
        // create new character <td> html element string and plug in the values
        var new_elem = `
            <td class="character" id="char_${index}">
                <img src="/static/images/character-${character_sheet.avatar_id}.png"/><br/>
                ${character_sheet.name} , ${character_sheet.hit_points_current}
                <div class="character-overlay" id="char_overlay_${index}"></div>
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
    for(var index=4; index < position_list.length; index++) {
        character_sheet = position_list[index];
        
        // create new character <td> html element string and plug in the values
        onclick_param = "";
        if (character_sheet.hit_points_current > 0) {
            onclick_param = `onclick=\"npc_clicked(${index})\"`;
        }
        var new_elem = `
            <td class="character" id="char_${index}" ${onclick_param}>
                <img src="/static/images/npc-${character_sheet.avatar_id}.png"/><br/>
                ${character_sheet.name} , ${character_sheet.hit_points_current}
                <div class="character-overlay" id="char_overlay_${index}"></div>
            </td>
            `;
        new_row += new_elem;
    }
    $("#npc_character_row").html(new_row);

}
    
    
//TODO Refactor for updated possition list
function display_character_health(position_list) {
    for (index=0; index<=position_list.length-1; index++) {
        character_sheet = position_list[index]
        var hit_points_total = character_sheet.hit_points_total;
        var hit_points_current = character_sheet.hit_points_current;
        var percentage = (hit_points_current/hit_points_total)*100;
        
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
        $("#char_" + index).css("border-color", color);
        //character_element.style["border-color"]=color;
        $("#char_" + index).css("opacity", opacity);
        //character_element.style["opacity"]=opacity;
    }
}


// TODO Refactor into generic select and highlight
function npc_clicked(position_index) {     
    if (npc_clicked_action == null){
        return;
    } else {
        npc_clicked_action(position_index);
        npc_clicked_action = null;
    }
}

function highlight_npc_characters(position_list, position_index= null) {
    if  (position_index==null) {
        for(index = 4; index <= position_list.length - 1; index++) {
            $("#char_" + index).css("border-color", "red");
        }
    } else {
        $("#char_" + position_index).css("border-color", "blue");
    }
}    


