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

// Bundle Bootstrap js, require JQuery slim
import './bootstrap-js/index.js'

// Bundle Bootstrap and custom styles
import './index.scss';
// import './custom.scss';

// Bundle Perfect Scrollbar
import PerfectScrollbar from 'perfect-scrollbar';

/**************************************************************************************************/

// Initialise Perfect Scrollbar on the left sidebar
const ps = new PerfectScrollbar('#left-sidebar-scroll');

$(document).ready(function () {
    // Open/Close left sidebar
    $('#close-left-sidebar').on('click', function () {
	$('#left-sidebar').removeClass('active');
	$('#body-content').addClass('body-content-expanded');
	setTimeout(function() {
	    $('#open-left-sidebar').parent().fadeIn(500);
	}, 280);

        // $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
    $('#open-left-sidebar').on('click', function () {
	$('#open-left-sidebar').parent().toggle();
	$('#body-content').removeClass('body-content-expanded');
	$('#left-sidebar').addClass('active');
    });


    // Open/Close sub-menus in sidebar
    $('ul.sidebar-elements li.parent a').on('click', function () {
	var li = $(this).parent();
	var ul = li.children().eq(1); // get second child
	ul.slideToggle(100); // ms  animate height
	li.toggleClass('open');
    });
});
