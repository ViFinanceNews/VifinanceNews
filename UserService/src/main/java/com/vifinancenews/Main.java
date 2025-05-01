package com.vifinancenews;

import com.vifinancenews.user.controllers.AvatarController;
import com.vifinancenews.user.controllers.UserController;

import io.javalin.Javalin;
import io.javalin.http.staticfiles.Location;

public class Main {
    public static void main(String[] args) {
        Javalin app = Javalin.create(config -> {
            // CORS and Routing Optimizations
            config.router.contextPath = "/";
            config.router.treatMultipleSlashesAsSingleSlash = true;

            // Enable Brotli & Gzip Compression
            config.http.brotliAndGzipCompression();

            // Static Files (relative to project root)
            config.staticFiles.add(staticFileConfig -> {
                staticFileConfig.hostedPath = "/"; // URL path for static files
                staticFileConfig.directory = "static"; // Ensure `/static` is accessible
                staticFileConfig.location = Location.CLASSPATH;
            });
        
            // Request Settings
            config.http.asyncTimeout = 30000; // 30 sec timeout
            config.http.maxRequestSize = 10_000_000L; // 10MB max request size
        }).start(6998);

        app.before(ctx -> {
            // CORS Settings
            ctx.header("Access-Control-Allow-Origin", "*"); // Allow all origins
            ctx.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
            ctx.header("Access-Control-Allow-Headers", "Content-Type, Authorization, Cookie"); // Include 'Cookie' in allowed headers

            // Session settings: Add cookie for session expiration
            ctx.cookie("session_timeout", String.valueOf(System.currentTimeMillis()), 600); // Session timeout in seconds
        });

        // **User Routes**
        app.get("/api/user/profile", UserController.getUserProfile);
        app.put("/api/user/update", UserController.updateUserProfile);
        app.delete("/api/user/delete", UserController.deleteUser);

        // Avatar Routes
        app.post("/api/avatar/upload", AvatarController.uploadAvatar);

        System.out.println("Server running on http://localhost:6998");
    }

}
