const API_URL = "http://localhost:8080/api/user"; // Ensure this matches the backend route

// Register User
function registerUser() {
    const data = new URLSearchParams();
    data.append("email", document.getElementById("regEmail").value);
    data.append("password", document.getElementById("regPassword").value);
    data.append("userName", document.getElementById("regUserName").value);
    data.append("avatarLink", document.getElementById("regAvatarLink").value);
    data.append("bio", document.getElementById("regBio").value);

    fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data.toString(),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to register');
        }
        return response.text();
    })
    .then(data => {
        document.getElementById("regMsg").textContent = 'Registration successful!';
    })
    .catch(error => {
        document.getElementById("regMsg").textContent = 'Error: ' + error.message;
    });
}

// Login User
async function loginUser() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const otp = document.getElementById("loginOtp").value;

    const data = new URLSearchParams();
    data.append("email", email);
    data.append("password", password);
    data.append("otp", otp);

    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        credentials: "include",  // Required for session-based authentication
        body: data.toString()
    });

    const message = await response.text();
    const loginMsgElement = document.getElementById("loginMsg");

    // Handle the response from the server
    if (response.ok) {
        // Login successful
        loginMsgElement.textContent = "Login successful! Session started.";
        // Show the logout button after login
        document.getElementById("logoutBtn").style.display = "block";
    } else {
        // Handle OTP required scenario
        if (message.includes("OTP required")) {
            loginMsgElement.textContent = "OTP has been sent to your email. Please enter it below.";
            // Show OTP input field and hide password field
            document.getElementById("loginPassword").style.display = "none";
            document.getElementById("otpSection").style.display = "block";
        } else {
            // Handle login failure or invalid credentials
            loginMsgElement.textContent = "Invalid credentials or OTP required.";
        }
    }
}

// Get Profile Info
async function fetchProfile() {
    const response = await fetch(`${API_URL}/profile`, {
        method: 'GET',
        credentials: 'include',  // Ensure session cookie is included
    });

    const profileMsgElement = document.getElementById("profileMsg");

    if (response.ok) {
        const profileData = await response.text();
        profileMsgElement.textContent = profileData;  // Display profile data as received from backend
    } else {
        profileMsgElement.textContent = "Error fetching profile. Please log in first.";
    }
}

// Logout User
async function logoutUser() {
    const response = await fetch(`${API_URL}/logout`, {
        method: 'POST',
        credentials: 'include',  // Ensure session cookie is included
    });

    const logoutMsgElement = document.getElementById("logoutMsg");
    const logoutBtnElement = document.getElementById("logoutBtn");

    if (response.ok) {
        logoutMsgElement.textContent = "Logged out successfully.";
        logoutMsgElement.style.display = "block";
        // Hide the logout button after logout
        logoutBtnElement.style.display = "none";
        // Reset login fields and hide OTP section
        document.getElementById("loginEmail").value = "";
        document.getElementById("loginPassword").value = "";
        document.getElementById("loginOtp").value = "";
        document.getElementById("otpSection").style.display = "none";
        document.getElementById("loginPassword").style.display = "block";
    } else {
        logoutMsgElement.textContent = "Error logging out.";
        logoutMsgElement.style.display = "block";
    }
}
