
async function handleFileUpload() {
    const fileInput = document.getElementById('file-upload');
    const message = document.getElementById('upload-message');

    if (fileInput.files.length === 0) {
        message.textContent = "Please select a file to upload.";
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);  // Append the selected file

    try {
        const response = await fetch('http://localhost:8080/uploadfile/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to upload');
        }

        const data = await response.json();  // JSON response containing summary
        message.textContent = "File uploaded successfully!";
        setTimeout(() => {
            window.location.href = "main.html";  // Redirect to main.html
        }, 2000);

    } catch (error) {
        message.textContent = "Error uploading file. Please try again.";
    }
}

document.getElementById('upload-btn').addEventListener('click', handleFileUpload);
