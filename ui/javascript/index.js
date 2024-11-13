document.getElementById("settings-btn").onclick = function() {
    document.getElementById("popup").style.display = "block";
};

document.getElementById("close-popup").onclick = function() {
    document.getElementById("popup").style.display = "none";
};


window.onclick = function(event) {
    const popup = document.getElementById("popup");
    if (event.target === popup) {
        popup.style.display = "none";
    }
};


document.getElementById("max-tokens").oninput = function() {
    document.getElementById("max-tokens-value").textContent = this.value;
};

document.getElementById("temperature").oninput = function() {
    document.getElementById("temperature-value").textContent = this.value;
};

document.getElementById("num-messages").oninput = function() {
    document.getElementById("num-messages-value").textContent = this.value;
};


document.getElementById("save-settings").onclick = function() {
    alert("Settings saved!");
    document.getElementById("popup").style.display = "none";
};


function showTab(tab) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');

    tabs.forEach(t => {
        t.classList.remove('active');
    });

    buttons.forEach(b => {
        b.classList.remove('active');
    });

    document.getElementById(tab).classList.add('active');
    event.target.classList.add('active');
}


document.getElementById("upload-btn").onclick = function() {
    const fileInput = document.getElementById("file-upload");
    const message = document.getElementById("upload-message");
    if (fileInput.files.length > 0) {
        message.textContent = `File "${fileInput.files[0].name}" uploaded successfully!`;
        setTimeout(() => {
            window.location.href = "main.html";
        }, 2000);
    } else {
        message.textContent = "Please select a file to upload.";
    }
};


document.getElementById("db-form").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    const host = document.getElementById("db-host").value;
    const port = document.getElementById("db-port").value;
    const user = document.getElementById("db-user").value;
    const password = document.getElementById("db-password").value;
    const dbName = document.getElementById("db-name").value;


    alert(`Connecting to database ${dbName} at ${host}:${port} with user ${user}.`);
    document.getElementById("connect-message").textContent = "Connection attempt initiated.";


    setTimeout(() => {
        window.location.href = "main.html";
    }, 2000);
};
