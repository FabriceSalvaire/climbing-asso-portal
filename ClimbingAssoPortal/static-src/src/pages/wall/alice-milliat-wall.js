/***************************************************************************************************
 *
 * Climbing Asso Portal
 * Copyright (C) 2018 Fabrice Salvaire
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

/**************************************************************************************************/

export
const alice_milliat_wall_line_position = {
    image_width  : 328,
    image_height : 1000,
    font_size : 16, // taille du n° en pixel
    y : 298, // ligne des n°
    x: [
	47, // couloir 0 inutilisé
	65, // 1
	93,
	121,
	149,
	177,
	209,
	241,
	273,
	293,
	317, // 10
	341,
	357,
	373,
	397,
	417,
	437,
	457,
	477,
	504,
	524, // 20
	544,
	564,
	584,
	604,
	631,
	651,
	671,
	691,
	711,
	730, // 30
	750,
	770,
	790,
	806,
	823,
	839,
	859,
	875,
	892,
	908, // 40
	924,
	941,
	957,
	973,
	991
    ]
};

/**************************************************************************************************/

function complete_wall(wall) {
    var new_wall = [];
    var previous_line = null;
    wall.map(line => {
	var line_number = new_wall.length + 1;
	if (line.line_number > line_number)
	    for (; line_number < line.line_number; line_number++)
		new_wall.push({ ...previous_line, line_number });
	new_wall.push(line);
	previous_line = line;
    });

    return new_wall;
}

/**************************************************************************************************/


// Fixme: missing lines ???
export
var alice_milliat_wall_line_profiles = complete_wall([
    { line_number: 1, sector:'Grande Dalle'    , profile:'Arète'   , inclination:'Dalle Douce' },
    { line_number: 2, sector:'Grande Dalle'    , profile:'Plan'    , inclination:'Dalle Douce' },
    { line_number: 3, sector:'Grande Dalle'    , profile:'Arète'   , inclination:'Dalle Douce' },

    { line_number: 4, sector:'Petit Mur'       , profile:'Dièdre'  , inclination:'Vertical' },
    { line_number: 5, sector:'Petit Mur'       , profile:'Plan'    , inclination:'Vertical' },
    // { line_number: 6, sector:'Petit Mur'       , profile:'Plan'    , inclination:'Vertical' },
    { line_number: 7, sector:'Petit Mur'       , profile:'Dièdre'  , inclination:'Vertical' },

    { line_number: 8, sector:'Dalle Brisée'    , profile:'Arète'   , inclination:'Dalle Forte' },
    { line_number: 9, sector:'Dalle Brisée'    , profile:'Plan'    , inclination:'Dalle Forte' },
    { line_number:10, sector:'Dalle Brisée'    , profile:'Arète'   , inclination:'Dalle Forte' },

    { line_number:11, sector:'Creux'           , profile:'Dièdre'  , inclination:'Verticale Corniche' },
    { line_number:12, sector:'Creux'           , profile:'Plan'    , inclination:'Verticale Corniche' },
    { line_number:13, sector:'Creux'           , profile:'Dièdre'  , inclination:'Devers Doux' },

    { line_number:14, sector:'Relief'          , profile:'Plan'    , inclination:'Devers' },
    // { line_number:15, sector:'Relief'          , profile:'Plan'    , inclination:'Devers' },
    { line_number:16, sector:'Relief'          , profile:'Arète'   , inclination:'Devers' },
    { line_number:17, sector:'Relief'          , profile:'Plan'    , inclination:'Devers' },
    { line_number:18, sector:'Relief'          , profile:'Arète'   , inclination:'Devers' },

    { line_number:19, sector:'Devers Concave'  , profile:'Dièdre'  , inclination:'Devers Doux' },
    { line_number:20, sector:'Devers Concave'  , profile:'Plan'    , inclination:'Devers Doux' },
    // { line_number:21, sector:'Devers Concave'  , profile:'Plan'    , inclination:'Devers Doux' },
    // { line_number:22, sector:'Devers Concave'  , profile:'Plan'    , inclination:'Devers Doux' },
    // { line_number:23, sector:'Devers Concave'  , profile:'Plan'    , inclination:'Devers Doux' },
    { line_number:24, sector:'Devers Concave'  , profile:'Arète'   , inclination:'Devers Doux' },
    { line_number:25, sector:'Devers Concave'  , profile:'Plan'   , inclination:'Devers Doux' },
    // { line_number:26, sector:'Devers Concave'  , profile:'Plan'   , inclination:'Devers Doux' },
    // { line_number:27, sector:'Devers Concave'  , profile:'Plan'   , inclination:'Devers Doux' },
    // { line_number:28, sector:'Devers Concave'  , profile:'Plan'   , inclination:'Devers Doux' },
    // { line_number:29, sector:'Devers Concave'  , profile:'Plan'   , inclination:'Devers Doux' },
    // { line_number:30, sector:'Devers Concave'  , profile:'Plan'    , inclination:'Devers Doux' },
    { line_number:31, sector:'Devers Concave'  , profile:'Dièdre'  , inclination:'Devers Doux' },

    { line_number:33, sector:'Coin'            , profile:'Plan'    , inclination:'Vertical Long' },
    // { line_number:32, sector:'Coin'            , profile:'Plan'    , inclination:'Vertical Long' },
    // { line_number:34, sector:'Coin'            , profile:'Plan'    , inclination:'Vertical Long' },
    { line_number:35, sector:'Coin'            , profile:'Dièdre'  , inclination:'Devers Doux' },

    { line_number:36, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    // { line_number:37, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    // { line_number:38, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    // { line_number:39, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    // { line_number:40, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    // { line_number:41, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers' },
    { line_number:42, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers Maxi' },
    // { line_number:43, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers Maxi' },
    { line_number:44, sector:'Grand Devers'    , profile:'Plan'    , inclination:'Devers Maxi'}
]);

// alice_milliat_wall_line_profiles.map(line => console.log(line));
