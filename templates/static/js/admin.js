var yql_console = 'http://developer.yahoo.com/yql/console/#h=';
var yql_query_template = 'SELECT * FROM meme.search(#highlight_amount#) WHERE query="#highlight_query#"';
var meme_search_template = 'http://meme.yahoo.com/search/?q=#highlight_query#';

var generate_bookmarklet = function() {
	var js = $('#bookmarklet_js').val();
	js = js.replace('#username#', $('#meme_username').val());
	$('#bookmarklet').attr('href', js);
	$('#bookmarklet_text').show();
};

var update_highlight_query = function(display_warning) {
	var new_query = yql_query_template;
	new_query = new_query.replace('#highlight_amount#', $('#highlight_amount').val());
	new_query = new_query.replace('#highlight_query#', $('#highlight_query').val());
	$('#yql_query').html(new_query);
	$('#yql_query_link').attr('href', yql_console + new_query.replace('=', '%3D'));

	var new_search = meme_search_template.replace('#highlight_query#', $('#highlight_query').val());
	$('#meme_search').html(new_search);
	$('#meme_search_link').attr('href', new_search);

	if (display_warning) {
		$('#highlight_warning').show();
	}
};

var highlight_submit = function() {
	var query = $('#highlight_query').val();
	var amount = $('#highlight_amount').val();
	var valid_amount = /^[1-9]{1}$/g;

	if ((query == '') || (amount == '')) {
		alert('You need to fill "Meme Query" and "Max. results" fields.');
	} else if (!valid_amount.test(amount)) {
		alert('"Max. results" field only supports numeric values (> 0).');
	} else {
		document.forms['highlight_form'].submit();
	}
};

$(document).ready(function() {
	$('#generate_bookmarklet').click(function(){ generate_bookmarklet() });
	$('#highlight_query').keyup(function(){ update_highlight_query(true); });
	$('#highlight_query').keydown(function(){ update_highlight_query(true); });
	$('#highlight_amount').keyup(function(){ update_highlight_query(true); });
	$('#highlight_amount').keydown(function(){ update_highlight_query(true); });
	$('#highlight_submit').click(function(){ highlight_submit(); });
	update_highlight_query(false);
});