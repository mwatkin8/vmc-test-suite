
window.onload = function() {
	//Display file in html
	var fileInput = document.getElementById('fileInput');
	var inDisplayArea = document.getElementById('inDisplayArea');

	fileInput.addEventListener('change', function(e) {
		var file_in = fileInput.files[0];
		var reader = new FileReader();

		reader.onload = function(e) {
			inDisplayArea.innerText = reader.result;
		}
		reader.readAsText(file_in);
		}
	});
}
