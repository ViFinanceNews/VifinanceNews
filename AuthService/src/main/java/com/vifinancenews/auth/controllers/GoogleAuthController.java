package com.vifinancenews.auth.controllers;

import com.vifinancenews.auth.services.GoogleAuthService;
import com.vifinancenews.auth.services.AuthenticationService;
import com.vifinancenews.common.models.Identifier;
import com.vifinancenews.common.daos.IdentifierDAO;
import com.vifinancenews.common.utilities.RedisSessionManager;
import io.javalin.http.Handler;

import java.util.Map;
import java.util.UUID;

public class GoogleAuthController {

    private static final AuthenticationService authService = new AuthenticationService();

    public static Handler handleGoogleLogin = ctx -> {
        try {
            String idToken = ctx.body(); // Get the ID token from the request body
            
            // Step 1: Validate token and extract email
            String email = GoogleAuthService.getGoogleUserEmail(idToken);
            if (email == null) {
                ctx.status(400).json(Map.of("error", "Invalid Google token"));
                return;
            }

            // Step 2: Check if user exists
            Identifier existingUser = IdentifierDAO.getIdentifierByEmail(email);

            // Step 3: If not, register as a new Google user
            if (existingUser == null) {
                boolean success = authService.registerUser(email, null, email, null, null, "google");
                if (!success) {
                    ctx.status(400).json(Map.of("error", "Google login failed"));
                    return;
                }
                existingUser = IdentifierDAO.getIdentifierByEmail(email); // Fetch the newly created user
            }

            // Step 4: Create Redis-backed session
            UUID userId = existingUser.getId();
            String sessionId = UUID.randomUUID().toString();
            RedisSessionManager.createSession(Map.of("sessionId", sessionId, "userId", userId.toString()));

            // Step 5: Set session ID in cookie
            ctx.cookie("SESSION_ID", sessionId, 3600); // 1 hour

            // Step 6: Return success response
            ctx.status(200).json(Map.of("message", "Google login successful", "userId", userId.toString()));
        } catch (Exception e) {
            ctx.status(500).json(Map.of("error", "Google login error", "details", e.getMessage()));
        }
    };
}
