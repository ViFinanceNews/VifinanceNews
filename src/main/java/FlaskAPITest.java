import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

import org.json.JSONArray;
import org.json.JSONObject;

public class FlaskAPITest {
    
    public static void main(String[] args) {
        String baseUrl = "http://127.0.0.1:5000"; // Flask default localhost

        // Test Homepage
        // sendGetRequest(baseUrl + "/home_page");

        // Test Search with User Query
        sendGetRequest(baseUrl + "/search_result/oil_price");
    }

    public static void sendGetRequest(String requestUrl) {
        try {
            URL url = new URL(requestUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            int responseCode = conn.getResponseCode();
            System.out.println("GET Response Code: " + responseCode);
        
            printResponse(conn);
            // List<HashMap<String, String>> responseResult = getResponse(conn);
            // System.out.println(responseResult);
          
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void sendPostRequest(String requestUrl) {
        try {
            URL url = new URL(requestUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

            int responseCode = conn.getResponseCode();
            System.out.println("POST Response Code: " + responseCode);
            printResponse(conn);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void printResponse(HttpURLConnection conn) throws IOException {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String inputLine;
            StringBuilder response = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            // System.out.println("Response: " + response);
            
            // System.out.println(response.toString());
            String resStr = response.toString();
            String removeQuote = resStr.substring(1,resStr.length()-1);
            Properties prop = new Properties();
            prop.load(new StringReader("key=" + removeQuote));
            String decodedString = prop.getProperty("key");
            // System.out.println(decodedString); // Output: Hello © World

            
            // System.out.println(formattedString);
            String cleanStr = decodedString.replace("\n", System.lineSeparator());
            System.out.println(cleanStr);
            JSONArray jsonArr = new JSONArray(decodedString);
            // System.out.println(formattedString);
            // System.out.println(jsonArr.toString());
        }
    }


    public static List<HashMap<String, String>> getResponse(HttpURLConnection conn) throws IOException {
        List<HashMap<String, String>> result = new ArrayList<>();

        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String inputLine;
            StringBuilder response = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            // Convert response to JSON
            JSONArray jsonArray = new JSONArray(response.toString());

            // Parse JSON array into a list of HashMaps
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                HashMap<String, String> map = new HashMap<>();

                for (String key : jsonObject.keySet()) {
                    map.put(key, jsonObject.getString(key));
                }

                result.add(map);
            }
        }

        return result;
    }

}