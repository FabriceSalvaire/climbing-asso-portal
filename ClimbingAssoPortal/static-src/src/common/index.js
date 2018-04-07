import './bootstrap-js/index.js'
import './index.scss';
// import './custom.scss';

import PerfectScrollbar from 'perfect-scrollbar';

$(document).ready(function () {
    // $('#left-sidebar').mCustomScrollbar({
    //     // theme: 'minimal'
    // 	scrollbarPosition: "outside"
    // });

    $('#close-sidebar').on('click', function () {
	$('#left-sidebar').removeClass('active');
    });

    $('ul.sidebar-elements li.parent a').on('click', function () {
	var li = $(this).parent();
	var ul = $(this).parent().children().eq(1);
	ul.slideToggle(100);
	li.toggleClass('open');
    });

    $('#sidebarCollapse').on('click', function () {
        $('#left-sidebar').addClass('active');
        // $('.overlay').fadeIn();
        // $('.collapse.in').toggleClass('in');
        // $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    const ps = new PerfectScrollbar('#left-sidebar-scroll');
});
