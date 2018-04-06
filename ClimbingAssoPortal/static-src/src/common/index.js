import './bootstrap-js/index.js'
import './index.scss';
// import './custom.scss';


$(document).ready(function () {
    $('ul.sidebar-elements li.parent a').on('click', function () {
	$(this).parent().toggleClass('open');
    });
});
