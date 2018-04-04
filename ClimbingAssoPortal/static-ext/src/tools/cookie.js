/***************************************************************************************************
 *
 * Climbing Grade
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

function get_cookie(name) {
    if (!document.cookie)
	return null;

    const cookies = document.cookie.split(';')
	  .map(c => c.trim())
	  .filter(c => c.startsWith(name + '='));

    if (cookies.length === 0)
	return null;
    else
	return decodeURIComponent(cookies[0].split('=')[1]);
}

function get_cookie(name) {
    var cookie_value = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}

// var csrftoken = get_cookie('csrftoken');
// console.log("csrftoken", csrftoken);
