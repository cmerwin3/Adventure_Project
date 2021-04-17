# Adventure Project


## Overview
The Adventure Project is a full-stack web-based adventure game inspired by table top role-playing games and choose your own adventure stories. 


### Game Link 
Here is a link to a live version of the Adventure Project. Please feel free to register a username and password and enjoy the story.
[http://adventure.cameronmerwin.net/](http://adventure.cameronmerwin.net/)


### Technologies Used 
- Python/Django
- Javascript/JQuery
- HTML
- CSS
- SQLite
- JSON/JSON Schema
- AWS(Lightsail, Route53)


## Game Play
The game functions in two parts. The first is Script Mode which contains the dialog and narration of the story and where the player has the agency to select dialog options to continue the adventure. The second is Combat Mode which uses the statistics of the player characters against the automated non-player characters and allowing the player to make tactical choices with some randomized elements. 


## Architecture
The core functionality is carried out by three layers.
1. UI (Javascript, HTML, CSS)
    - A thin client with intuitive controls that use REST API to intitate actions with the server and display current game state.
	- Using a single [HTML page structure](https://github.com/cmerwin3/Adventure_Project/blob/master/ui/templates/home.html) the client is dynamically updated based on current game state. 
2. Server (Python/Django)
    - Views handle the REST API requests and save session data.
    - Services handle the business logic for script progression and combat actions.
    - Models define the structures for the business entities (ie Game Data, Player Charactes, Non-Player Characters, Class Levels, Items, and Spells).
3. Database (SQLite)


### Storyboard
Inspired by the branching stories of choose your own adventure books I created storyboards which contain a series of scripts coded within JSON files. A script is composed of a `background_image`, `npc_list`, `prompt`, and one or more `responses` each of which point to the next script in a branching tree of choices. Each script has a unique id with a hierarchical structure that not only inherets key information from the parent but is also used to organize each script within the JSON file. An example is 'Town.Mayor.1' The 'Mayor' is the child of 'Town' and will inherit the `background_image` and `npc_list` if not provided in it's own script, the same is true for '1' is the child of 'Town.Mayor'. JSON Schema is used to enforce correct JSON structure of the scripts. An example of a script file can be found [here](https://github.com/cmerwin3/Adventure_Project/blob/master/storyboard/town_script.json) .


### Characters and Combat
The abstract class of `Character` functions as the parent to the concrete classes `PC_Character` and `NPC_Character`. This structure can be found [here](https://github.com/cmerwin3/Adventure_Project/blob/master/character/models.py).

Inspired by the rules of table top role-playing games I wrote business logic to handle the functions used in combat mode. I created an array of character objects known as `position_list` so that the classes `PC_Character` and `NPC_Character` can be used by the same functions while remaining unique. Using `position_list` as the referance point for my variables allows me to have any character target any other character in any function that I create maintaining maximum flexibility. 


## REST API
The UI sends requests to the server to intiate actions with the server to get the game state. 
Many of the REST API responses include the following domain objects:
- `script_id` - Each step of the storyboard narration is defined as a "script" which includes a prompt and multiple responses for a user to select from. Each script is defined by a unique script_id
- `prompt` - Dialog and/or narration of the current script.
- `responses` - An array of the retort dialog and/or narration for the player to choose from.
- `position_list` - An array of character objects based on the current state of the game. There are always 4 player characters (PC) and 0-6 non-player characters (NPC). Each character object contains things like name, hit points, and other key data relevent to the buisness logic.
- `turn_order_list` - Upon intiation of combat the server randomly determines the order in which each character acts in each combat round. These numbers refer to the index into the position list.  


### Script Mode
**This URL loads the next requested script based on player dialog choice, upon load if no script is supplied the system will default to an introductory script.**
```
HTTP GET: {domain}/script/{script_id}

Success Response: HTTP 200 OK
{
    “script_id”: "town.intro",
    "background" : "town_background.jpg",
    “position_list”: [
		{			
			# pc 0 object
		},
		{
			# pc 1 object
		},
		{
			# pc 2 object
		},
		{
			# pc 3 object
		},
		{
			# npc 4 object
		},
	],
	"prompt": "You enter the southern gates of the mountain town. Near the center town square you see a small gatehring of people and facing them is a man in a tattered suit and tophat.",
	"responses": [ 
		{
			"response": "Ignore him and continue walking."
		},
		{
			"response": "Aproach the people and listen.",
		}
	]
}

```

**When a user clicks on a response this URL is sent to the server and the server responds with either the next script_id to load or combat_mode.**
```
HTTP GET: {domain}/script/{script_id}/{response_id}

Success Response: HTTP 200 OK
{
	“combat_mode”: true
(or)
	“next_script”: {script_id}
}
```


### Combat Mode


**When the server determines that combat_mode begins the UI sends this URL to initiate combat_mode.**
```
HTTP GET: {domain}combat/init/

Success Response: HTTP 200 OK
{
	“position_list”: [
		{			
			# pc 0 object
		},
		{
			# pc 1 object
		},
		{
			# pc 2 object
		},
		{
			# pc 3 object
		},
		{
			# npc 4 object
		},
	],
	"turn_order_list", [2, 4, 1, 0, 5],	
	"background" : "combat_background.jpg"
}

```


**This URL is used when the player selects an attack against an NPC.**
```
HTTP GET: {domain}/combat/attack/

Success Response: HTTP 200 OK
{
	"narration": "You attack the enemy with your sword and deal 10 damage.",
	“source_id”: 0
	"recipient_ids" : [ 4 ],
	"damage": 10,
	“natural”: 10
}

```


**During combat the UI calls this URL at the beginning of a turn in order for the server to determin one of four posibilities for the current turn. They are as follows:**
 - pc_turn - If it is a PCs turn and the PC has more than 0 hit points the server will await a choice from the UI.
 - npc_turn - If it is a NPCs turn and the NPC has more than 0 hit points the server will decide the actions of the NPC and return the results as npc_turn_data. 
 - skip_turn - If the current character has 0 hit points the server will flag the character as dead and return skip_turn_data.
 - end_combat- If all characters from either side are flagged as dead then the server will return end_combat_data.
```
HTTP GET: {domain}/combat/turn/

Success Response: HTTP 200 OK
{
	“current_turn”: 0,
	“turn_status”:     <choice of:> 
						“pc_turn”
						“npc_turn”
						“skip_turn”
						“end_combat”
	“npc_turn_data”: {
		"narration": "The enemy attacks you for 5 damage.",
		“source_id”: 4
		"recipient_ids" : [ 0 ],
		"damage": 5,
		“natural”: 10
	},
	“skip_turn_data”, {
		“status”: “dead”
		“narration: “The [name] is unmoving on the ground”
	}
	“end_combat_data” : {
		“conclusion”: “win” or “loss”
		“narration”: “You live to fight another day.” 
		“next_script”: “mine.exit”
	}
}
```


## Versions
- V1 (Current)- Initial release includes Storyboards, Combat, Game Data structure, and Automated NPCs. 
- V2 - Adding Spells, Items, more combat options, and a full story line.
- V3 - Restructre the game into a customizable experiance where the user can input their own scripts and images to create their own adventure. 

## Author
### Cameron Merwin 
[Linkedin Profile](https://www.linkedin.com/in/cameron-merwin-a4316320b/)

## License
This project is licensed under the [Apache License V2.0](https://github.com/cmerwin3/Adventure_Project/blob/master/LICENSE.txt)
