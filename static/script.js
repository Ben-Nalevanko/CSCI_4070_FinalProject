const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("upload-button");
const runButton = document.getElementById("run-button");

const algorithm = document.getElementById("algorithm-options");

uploadButton.addEventListener("click", () => {
	const file = fileInput.files[0];
	console.log("Test");

	if (file){
		const formData = new FormData();
		formData.append("file", file);
		console.log("Test");
		fetch("http://127.0.0.1:5000/load_data", {
			mode: "no-cors",
			method: "POST",
			body: formData,
		})

	}
});

runButton.addEventListener("click", async () => {
	console.log("Sending start POST");
	const requestData = {
		"algorithm": algorithm.value,
		"file": fileInput.files[0].name
	};
	console.log(requestData);

	fetch("http://127.0.0.1:5000/run", {
		method: "POST",
		headers: {
        		"Content-Type": "application/json",
      		},
		body: JSON.stringify(requestData),
	});
});
