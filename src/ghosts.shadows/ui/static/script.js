// Store token globally
let token = localStorage.getItem("access_token") || "";

// Event listeners for Enter key
document.getElementById("signup-username").addEventListener("keypress", handleEnter);
document.getElementById("signup-password").addEventListener("keypress", handleEnter);
document.getElementById("login-username").addEventListener("keypress", handleEnter);
document.getElementById("login-password").addEventListener("keypress", handleEnter);
document.getElementById("model-input").addEventListener("keypress", handleEnter);

// Handle Enter key press
function handleEnter(event) {
    if (event.key === "Enter") {
        if (event.target.closest("#signup")) {
            signup();
        } else if (event.target.closest("#login")) {
            login();
        } else if (event.target.closest("#query")) {
            generateContent();
        }
    }
}

// Signup function
async function signup() {
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;

    try {
        const response = await fetch("/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorDetail = await response.json();
            throw new Error(errorDetail.detail || "Signup failed");
        }

        const result = await response.json();
        document.getElementById("response-output").textContent = result.message;
    } catch (error) {
        document.getElementById("response-output").textContent = `Error: ${error.message}`;
    }
}

// Login function
async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    try {
        const response = await fetch("http://localhost:7860/token", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorDetail = await response.json();
            throw new Error(errorDetail.detail || "Login failed");
        }

        const result = await response.json();

        if (result.access_token) {
            token = result.access_token;
            localStorage.setItem("access_token", token);
            document.getElementById("response-output").textContent = `User "${username}" successfully logged in`;
        } else {
            document.getElementById("response-output").textContent = "Login failed: No access token received.";
        }
    } catch (error) {
        document.getElementById("response-output").textContent = `Error: ${error.message}`;
    }
}

async function generateContent() {
    const query = document.getElementById("model-input").value;
    const model = document.getElementById("model").value;

    console.debug('Generating content for query:', query);
    console.debug('Using model:', model);

    if (!token) {
        token = localStorage.getItem("access_token");
        console.debug('Token from localStorage:', token);

        if (!token) {
            console.error('Error: Not authenticated. Please log in.');
            document.getElementById("response-output").textContent = "Error: Not authenticated. Please log in.";
            return;
        }
    }

    try {
        console.debug('Sending request to server...');

        const response = await fetch(`http://localhost:5900/${model}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ query })
        });

        console.debug('Received response:', response);

        if (!response.ok) {
            console.error('Response was not OK:', response.status);
            const errorDetail = await response.json();
            console.debug('Error detail:', errorDetail);
            document.getElementById("response-output").textContent = `Error: ${errorDetail.detail || "Unknown error occurred"}`;
            return;
        }

        // Check the content type
        const contentType = response.headers.get("Content-Type");
        console.debug('Content-Type of the response:', contentType);

        if (contentType && contentType.startsWith("image")) {
            console.debug('Image content detected.');

            // Handle image response
            const blob = await response.blob();
            console.debug('Image blob received:', blob);

            const imgURL = URL.createObjectURL(blob);
            console.debug('Generated image URL:', imgURL);

            // Create and display the image
            const imgElement = document.createElement("img");
            imgElement.src = imgURL;
            imgElement.style.maxWidth = '100%';
            imgElement.style.height = 'auto';

            const outputElement = document.getElementById("response-output");
            outputElement.innerHTML = ''; // Clear previous content
            outputElement.appendChild(imgElement);

            console.debug('Image displayed successfully.');
        } else if (contentType && contentType.includes("application/json")) {
            console.debug('JSON content detected.');

            // Handle JSON response
            const result = await response.json();
            console.debug('JSON response:', result);

            if (result.message && (result.message.startsWith("http") || result.message.startsWith("data:image"))) {
                console.debug('Message contains an image URL or base64 string.');

                // Handle if the message is an image URL or base64 string
                const imgElement = document.createElement("img");
                imgElement.src = result.message;
                imgElement.style.maxWidth = '100%';
                imgElement.style.height = 'auto';

                const outputElement = document.getElementById("response-output");
                outputElement.innerHTML = '';
                outputElement.appendChild(imgElement);
                console.debug('Image displayed from JSON message.');
            } else {
                document.getElementById("response-output").textContent = result.message;
                console.debug('Text response:', result.message);
            }
        } else {
            console.error('Error: Unexpected content type.');
            document.getElementById("response-output").textContent = "Error: Unexpected content type.";
        }
    } catch (error) {
        console.error('Network error:', error);
        document.getElementById("response-output").textContent = `Network error: ${error.message}`;
    }
}
