package com.test_java;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class FlaskModelClient {

    private static final String BASE_URL = "http://127.0.0.1:8080";

    public static void main(String[] args) throws IOException {
        String sampleText = "Tôi rất hài lòng với sản phẩm này!";

        // Test sentiment endpoint
        System.out.println("🔍 Analyzing Sentiment:");
        JSONObject sentimentResult = postJson("/analyze-sentiment", sampleText);
        System.out.println(sentimentResult.toString(2));

        // Test embedding endpoint
        System.out.println("\n🔍 Getting Embedding:");
        JSONObject embeddingResult = postJson("/get-embedding", sampleText);
        System.out.println(embeddingResult.toString(2));
    }

    private static JSONObject postJson(String endpoint, String text) throws IOException {
        URL url = new URL(BASE_URL + endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        // Set headers
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        // Create JSON body
        JSONObject body = new JSONObject();
        body.put("text", text);

        // Send request
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = body.toString().getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        // Read response
        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
        }

        return new JSONObject(response.toString());
    }
}