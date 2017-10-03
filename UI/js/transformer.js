//
// Helper function allows use of "$()" instead of "document.getElementById()"
//
function $(id) { return document.getElementById(id) }

//
// When the page loads:
// 1. Set up external links as pop-ups
// 2. Replace unimplemented links with a message
// 3. Add onclick events to the navigation menu so when items are clicked they
//    are highlighted
//
window.onload = function() {
	// Loop through links
	links = document.getElementsByTagName('a')
	for(i=0; i<links.length; i++ ) {
		link = links[i]

		// Set up links with class="exLink" as full screen pop ups
		if(link.className && link.className.indexOf('exLink')>-1) {
			link.href = "javascript:void window.open('" + link.href
			link.href += "','','width='+screen.width+',height='+screen.height+',resizable=1,directories=1,menubar=1,toolbar=1,scrollbars=1').focus()"
		}

		// Set up links with class="popUp" as centered pop ups without toolbars
		if(link.className && link.className.indexOf('popUp')>-1) {
			x = Math.floor(screen.width/2) - 375
			y = Math.floor(screen.height/2) - 325
			link.href = "javascript:void window.open('" + link.href
			link.href += "','EMR','width=750,height=550,top='+y+',left='+x+',toolbar=0,scrollbars=1').focus()"
		}


		// All "Top" links in the document should select the Top (first) item in the nav menu
		if(endsWith(link.href,"#top")) {
			// Simulate a click on the "Top" nav item (which has an id of navTop)
			link.onclick = function() { selectFragment($("navTop")) }
		}
	}

	// Set up onclick events for links to fragments from the nav menu
	if($("nav")) {
		for(i=0; i<$("nav").childNodes.length; i++)
		$("nav").childNodes[i].childNodes[0].onclick = function() { selectFragment(this) }
	}
}

//
// Returns true if the string x ends with the string y
//
function endsWith(x, y) {
	if(x.length > y.length && x.substr(x.length-y.length,y.length) == y)
	return true
	else
	return false
}

//
// This event handler is called when a nav list item is clicked; it selects the
// appropriate menu item and unselects others
//
function selectFragment(el) {
	// Unselect all the items in the list
	for(i=0; i<$("nav").childNodes.length; i++)
	$("nav").childNodes[i].childNodes[0].className = ""

	// Select the clicked list item
	el.className = "selected"
}

var app = angular.module("toolApp", []);
app.controller('Ctrl', function($scope){
	$scope.tools = ["VEP", "None"];
	$scope.fields = [{
    id: 1,
    text: 'gene_symbol'
  }, {
    id: 2,
    text: 'biotype'
  }, {
    id: 3,
    text: 'gene_id'
  }, {
    id: 4,
    text: 'hgnc_id'
  }, {
    id: 5,
    text: 'transcript_id'
  }, {
    id: 6,
    text: 'cds_start'
  }, {
    id: 7,
    text: 'cds_end'
  }, {
    id: 8,
    text: 'variant_allele'
  }, {
    id: 9,
    text: 'impact'
  }, {
    id: 10,
    text: 'consequence_terms'
  }, {
    id: 11,
    text: 'gene_source_symbol'
  }];
  $scope.isChecked = function(id, matches) {
    var isChecked = false;
    angular.forEach(matches, function(match) {
      if (match === id) {
        isChecked = true;
      }
    });
    return isChecked;
  }
  $scope.tool = {
    fields: [1,2,3,4,5,6,7,8,9,10,11]
  };
});
app.controller("Ctrl", Ctrl);
