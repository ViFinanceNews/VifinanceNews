package com.test_java;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.net.URL;
import java.io.OutputStream;

public class GetCachedResultTest {

    public static void main(String[] args) {
        getCachedResult("giá xăng dầu");
        // voteArticle("https://vnexpress.net/bai-viet-4866570.html?commentid=59194192", -1);
    }
    public static void getCachedResult(String userQuery) {
        try {
            String requestUrl = "http://localhost:5001/get_cached_result";
            URL url = new URL(requestUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
    
            // 🔁 Use POST method
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; utf-8");
            connection.setRequestProperty("Accept", "application/json");
            connection.setDoOutput(true);
    
            // 📦 Build JSON payload
            String jsonInputString = String.format("{\"query\": \"%s\"}", userQuery);
    
            // 💥 Send request
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonInputString.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }
    
            // 📥 Read the response
            int responseCode = connection.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode);
    
            BufferedReader reader;
            if (responseCode >= 200 && responseCode < 300) {
                reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            } else {
                reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
            }
    
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line.trim());
            }
            reader.close();
            connection.disconnect();
    
            // 🧠 Print full response
            System.out.println("Response from Server:");
            System.out.println(response.toString());
    
            // 🧪 Parse and extract results
            try {
                JSONObject jsonResponse = new JSONObject(response.toString());
                if (jsonResponse.has("data")) {
                    JSONArray dataArray = jsonResponse.getJSONArray("data");
                    System.out.println("Extracted URLs:");
                    for (int i = 0; i < dataArray.length(); i++) {
                        System.out.println("- " + dataArray.getString(i));
                    }
                } else if (jsonResponse.has("error")) {
                    System.err.println("Server returned error: " + jsonResponse.getString("error"));
                }
            } catch (Exception jsonEx) {
                System.err.println("Failed to parse JSON response: " + jsonEx.getMessage());
            }
    
        } catch (Exception e) {
            System.err.println("Error while making POST request: " + e.getMessage());
            e.printStackTrace();
        }
    };
    
    public static void voteArticle(String url, int voteType) {

        try {
            // Define the endpoint
            URL endpoint = new URL("http://localhost:5001/vote");
            HttpURLConnection conn = (HttpURLConnection) endpoint.openConnection();

            // Configure POST request
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; utf-8");
            conn.setDoOutput(true);

            // Build JSON payload
            String jsonInputString = String.format(
                "{\"url\": \"%s\", \"vote_type\": %d}", url, voteType
            );

            // Send JSON payload
            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInputString.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }

            // Read response
            int responseCode = conn.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode);

            // Optional: Read response body if needed
            try (var reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line.trim());
                }
                System.out.println("Response: " + response.toString());
            }

            conn.disconnect();

        } catch (Exception e) {
            System.err.println("Error while sending vote request: " + e.getMessage());
            e.printStackTrace();
        }
    };

    
}
