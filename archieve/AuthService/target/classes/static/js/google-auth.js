function onGoogleSignIn(googleUser) {
    const idToken = googleUser.getAuthResponse().id_token;
    const email = googleUser.getBasicProfile().getEmail();
    handleGoogleLogin(idToken, email);
}

async function handleGoogleLogin(idToken, email) {
    const response = await fetch("/api/google-login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ idToken }),
        credentials: "include",
    });

    const result = await response.json();

    if (response.ok) {
        console.log(result.message);
        if (result.message === "User requires profile data") {
            window.location.href = "/profile-setup.html";
        } else {
            alert("Google login successful!");
            window.location.href = "/index.html";
        }
    } else {
        alert("Google login failed: " + result.error);
    }
}

// Render the Google button once the page and gapi are ready
window.addEventListener("load", () => {
    gapi.load("auth2", () => {
        gapi.auth2.init({
            client_id: "730255015972-m08dadflh0eatde4ij0tgacnb556939c.apps.googleusercontent.com"
        }).then(() => {
            gapi.signin2.render("google-login-btn", {
                onsuccess: onGoogleSignIn,
                theme: "dark",
                longtitle: true,
            });
        });
    });
});
