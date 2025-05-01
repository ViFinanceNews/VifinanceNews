package com.vifinancenews.user.controllers;

import com.vifinancenews.user.services.AccountService;
import com.vifinancenews.common.models.Account;
import com.vifinancenews.common.utilities.RedisSessionManager;
import io.javalin.http.Handler;

import java.util.Map;
import java.util.UUID;

public class UserController {

    private static final AccountService accountService = new AccountService();

    // Handler for retrieving user profile
    public static Handler getUserProfile = ctx -> {
        String sessionId = ctx.cookie("SESSION_ID"); // Updated to match cookie name
        if (sessionId == null) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        Map<String, Object> sessionData = RedisSessionManager.getSession(sessionId);
        if (sessionData == null || !sessionData.containsKey("userId")) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        UUID uuid = UUID.fromString(sessionData.get("userId").toString());
        Account account = accountService.getUserProfile(uuid);
        if (account == null) {
            ctx.status(404).result("User not found");
        } else {
            ctx.json(account);
        }
    };

    // Handler for updating user profile
    public static Handler updateUserProfile = ctx -> {
        String sessionId = ctx.cookie("SESSION_ID"); // Updated to match cookie name
        if (sessionId == null) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        Map<String, Object> sessionData = RedisSessionManager.getSession(sessionId);
        if (sessionData == null || !sessionData.containsKey("userId")) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        UUID uuid = UUID.fromString(sessionData.get("userId").toString());

        // Parse JSON request into a Map
        Map<String, String> requestData = ctx.bodyAsClass(Map.class);

        String userName = requestData.get("userName");
        String avatarLink = requestData.get("avatarLink"); // Can be null
        String bio = requestData.get("bio"); // Can be null

        // Validate required field
        if (userName == null || userName.isEmpty()) {
            ctx.status(400).result("Username cannot be empty");
            return;
        }

        boolean success = accountService.updateUserProfile(uuid, userName, avatarLink, bio);

        if (success) {
            ctx.status(200).result("Profile updated successfully");
        } else {
            ctx.status(400).result("Failed to update profile");
        }
    };

    // Handler for soft deleting user
    public static Handler deleteUser = ctx -> {
        String sessionId = ctx.cookie("SESSION_ID"); // Updated to match cookie name
        if (sessionId == null) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        Map<String, Object> sessionData = RedisSessionManager.getSession(sessionId);
        if (sessionData == null || !sessionData.containsKey("userId")) {
            ctx.status(401).result("Unauthorized");
            return;
        }

        UUID uuid = UUID.fromString(sessionData.get("userId").toString());
        boolean softDeleted = accountService.softDeleteUserById(uuid);  // Call soft delete method

        if (softDeleted) {
            // Invalidate the session in Redis
            RedisSessionManager.destroySession(sessionId);
            ctx.status(200).result("Your account has been deactivated for 30 days before permanent deletion. You can restore it during this period.");
        } else {
            ctx.status(400).result("Failed to soft delete user.");
        }
    };
}
