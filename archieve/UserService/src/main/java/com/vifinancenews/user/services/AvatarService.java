package com.vifinancenews.user.services;

import com.vifinancenews.common.config.S3Config;
import net.coobird.thumbnailator.Thumbnails;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.UUID;

public class AvatarService {

    private final S3Client s3 = S3Config.getClient();
    private final String bucketName = S3Config.getBucketName();
    private final String baseUrl = S3Config.getBaseUrl();

    // Maximum width and height for the resized image
    private static final int MAX_WIDTH = 200;
    private static final int MAX_HEIGHT = 200;

    public String uploadAvatar(UUID userId, InputStream avatarStream, String fileName, String contentType) {
        try {
            // Resize the image using Thumbnailator
            InputStream resizedImageStream = resizeImage(avatarStream, MAX_WIDTH, MAX_HEIGHT);

            // Generate a safe file name
            String fileExtension = fileName.substring(fileName.lastIndexOf('.')); // ".jpg" or ".png"
            String safeFileName = UUID.randomUUID() + fileExtension;
            String key = "avatars/" + userId + "/" + safeFileName;

            // Build the PutObjectRequest
            PutObjectRequest putReq = PutObjectRequest.builder()
                    .bucket(bucketName)
                    .key(key)
                    .contentType(contentType != null ? contentType : "application/octet-stream")
                    .build();

            // Upload the resized image to S3
            try {
                System.out.println("Uploading to S3...");
                s3.putObject(putReq, RequestBody.fromInputStream(resizedImageStream, resizedImageStream.available()));
                System.out.println("Upload successful.");
            } catch (Exception e) {
                System.err.println("Error uploading to S3: " + e.getMessage());
                e.printStackTrace();
            }
            
            // Return the full URL to the uploaded avatar
            return baseUrl + key;
        } catch (Exception e) {
            // Log the exception and return null for the failed upload
            System.err.println("Error uploading avatar: " + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }

    // Resize the image to fit within MAX_WIDTH and MAX_HEIGHT
    private InputStream resizeImage(InputStream originalImage, int maxWidth, int maxHeight) throws Exception {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        Thumbnails.of(originalImage)
                .size(maxWidth, maxHeight) // Resize to fit within the specified width/height
                .keepAspectRatio(true) // Preserve aspect ratio
                .outputQuality(0.8) // Optional: adjust output quality (0.0 to 1.0)
                .toOutputStream(outputStream);
        return new ByteArrayInputStream(outputStream.toByteArray());
    }
}
