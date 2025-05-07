package com.vifinancenews.user.controllers;

import com.vifinancenews.user.services.AvatarService;
import io.javalin.http.UploadedFile;
import io.javalin.http.Handler;

import java.io.InputStream;
import java.util.Map;
import java.util.UUID;

public class AvatarController {

    private static final AvatarService avatarService = new AvatarService();

    public static Handler uploadAvatar = ctx -> {
        String userId = ctx.sessionAttribute("userId"); // May be null for guest
    
        UploadedFile uploadedFile = ctx.uploadedFile("avatar");
        if (uploadedFile == null) {
            ctx.status(400).json(Map.of("error", "No avatar file uploaded"));
            return;
        }
    
        // Validate file type
        String contentType = uploadedFile.contentType();
        if (!contentType.startsWith("image/")) {
            ctx.status(400).json(Map.of("error", "Only image files are allowed"));
            return;
        }
    
        // Validate file size (e.g., max 5MB)
        if (uploadedFile.size() > 5_000_000L) { // 5MB max size
            ctx.status(400).json(Map.of("error", "File size exceeds the 5MB limit"));
            return;
        }
    
        InputStream avatarStream = uploadedFile.content();
        String originalFilename = uploadedFile.filename();
    
        try {
            UUID uuid = userId != null ? UUID.fromString(userId) : UUID.randomUUID(); // guest fallback
            String avatarUrl = avatarService.uploadAvatar(uuid, avatarStream, originalFilename, contentType);
    
            if (avatarUrl != null) {
                ctx.status(200).json(Map.of(
                    "message", "Avatar uploaded successfully",
                    "avatarUrl", avatarUrl
                ));
            } else {
                ctx.status(500).json(Map.of("error", "Failed to upload avatar"));
            }
    
        } catch (Exception e) {
            e.printStackTrace();
            ctx.status(500).json(Map.of("error", "Server error", "details", e.getMessage()));
        }
    };
    
}
