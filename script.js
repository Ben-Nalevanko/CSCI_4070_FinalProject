const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("upload-button");
const algorithm = "linreg";

uploadButton.addEventListener("click", () => {
	const file = fileInput.files[0];
	console.log("Test");
	if (file){
		const formData = new FormData();
		formData.append("file", file);
		formData.append("algorithm", algorithm);
		console.log("Test");
		fetch("http://127.0.0.1:5000/load_data", {
			mode: "no-cors",
			method: "POST",
			headers: {
				"Contents-Type": "application/json"
			},
			body: formData,
		})

	}
});
