export
var alice_milliat_wall_line_position = {
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
}

// Fixme: missing lines ???
export
var alice_milliat_wall_line_profiles = [
    { line_number: 1, sector:'Grande Dalle'    , profil:'Arète'   , inclination:'Dalle Douce' },
    { line_number: 2, sector:'Grande Dalle'    , profil:'Plan'    , inclination:'Dalle Douce' },
    { line_number: 3, sector:'Grande Dalle'    , profil:'Arète'   , inclination:'Dalle Douce' },
    { line_number: 4, sector:'Petit Mur'       , profil:'Dièdre'  , inclination:'Vertical' },
    { line_number: 6, sector:'Petit Mur'       , profil:'Plan'    , inclination:'Vertical' },
    { line_number: 7, sector:'Petit Mur'       , profil:'Dièdre'  , inclination:'Vertical' },
    { line_number: 8, sector:'Dalle Brisée'    , profil:'Arète'   , inclination:'Dalle Forte' },
    { line_number: 9, sector:'Dalle Brisée'    , profil:'Plan'    , inclination:'Dalle Forte' },
    { line_number:10, sector:'Dalle Brisée'    , profil:'Arète'   , inclination:'Dalle Forte' },
    { line_number:11, sector:'Creux'           , profil:'Dièdre'  , inclination:'Verticale Corniche' },
    { line_number:12, sector:'Creux'           , profil:'Plan'    , inclination:'Verticale Corniche' },
    { line_number:13, sector:'Creux'           , profil:'Dièdre'  , inclination:'Devers Doux' },
    { line_number:15, sector:'Relief'          , profil:'Plan'    , inclination:'Devers' },
    { line_number:16, sector:'Relief'          , profil:'Arète'   , inclination:'Devers' },
    { line_number:17, sector:'Relief'          , profil:'Plan'    , inclination:'Devers' },
    { line_number:18, sector:'Relief'          , profil:'Arète'   , inclination:'Devers' },
    { line_number:19, sector:'Devers Concave'  , profil:'Dièdre'  , inclination:'Devers Doux' },
    { line_number:23, sector:'Devers Concave'  , profil:'Plan'    , inclination:'Devers Doux' },
    { line_number:24, sector:'Devers Concave'  , profil:'Arète'   , inclination:'Devers Doux' },
    { line_number:30, sector:'Devers Concave'  , profil:'Plan'    , inclination:'Devers Doux' },
    { line_number:31, sector:'Devers Concave'  , profil:'Dièdre'  , inclination:'Devers Doux' },
    { line_number:34, sector:'Coin'            , profil:'Plan'    , inclination:'Vertical Long' },
    { line_number:35, sector:'Coin'            , profil:'Dièdre'  , inclination:'Devers Doux' },
    { line_number:41, sector:'Grand Devers'    , profil:'Plan'    , inclination:'Devers' },
    { line_number:44, sector:'Grand Devers'    , profil:'Plan'    , inclination:'Devers Maxi'}
]
