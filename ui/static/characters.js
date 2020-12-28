
        
    var character_list = [ { 
            name : "Cameron",
            hit_points_total: 50,
            hit_points_current: 0
        }, { 
            name : "Charlie",
            hit_points_total: 50,
            hit_points_current: 40
        }
    ];

    function load_character_sheet(character_id) {
        // make REST API call to get full character sheet
        var url = "character/" + character_id;
        $.getJSON( url )
            .done(function( json ) {
                console.log( "Character JSON loaded: " + json.id + " (" + json.name + ")");

                // create new character <td> html element string and plug in the values
                var new_elem = `
                    <td class="character" id="char_${json.id}">
                        <img src="/static/images/character-${json.avatar_id}.png"/><br/>
                        ${json.name}
                        <div class="character-tooltip">
                            Class: ${json.class_level.class_type}<br/>
                            Level: ${json.class_level.level}<br/>
                            Strength: ${json.strength}<br/>
                            Dexterity: ${json.dexterity}<br/>
                            Constitution: ${json.constitution}<br/>
                            Intelligence: ${json.intelligence}<br/>
                            Wisdom: ${json.wisdom}<br/>
                            Charisma: ${json.charisma}<br/>
                            Hit Points Total: ${json.hit_points_total}<br/>
                            Hit Points Current: ${json.hit_points_current}
                        </div>
                    </td>
                    `;

                // insert new element string into table html on the page
                $(".pc_character_row").append(new_elem);
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
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

    $(document).ready(function() {
        load_character_sheet(1);
        display_character_health();
        load_script(1);
    });
