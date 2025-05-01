package com.vifinancenews.auth.services;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.auth.oauth2.GoogleTokenResponse;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.oauth2.Oauth2;
import com.google.api.services.oauth2.model.Userinfo;
import io.github.cdimascio.dotenv.Dotenv;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.List;

public class GoogleAuthService {

    private static final Dotenv dotenv = Dotenv.load();

    private static final String CLIENT_ID = dotenv.get("GOOGLE_CLIENT_ID");
    private static final String CLIENT_SECRET = dotenv.get("GOOGLE_CLIENT_SECRET");
    private static final String REDIRECT_URI = dotenv.get("GOOGLE_REDIRECT_URI");

    private static final List<String> SCOPES = List.of(
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
    );

    private static final JsonFactory JSON_FACTORY = GsonFactory.getDefaultInstance();

    public static GoogleAuthorizationCodeFlow getGoogleAuthFlow() throws IOException, GeneralSecurityException {
        GoogleClientSecrets clientSecrets = new GoogleClientSecrets()
                .setInstalled(new GoogleClientSecrets.Details()
                        .setClientId(CLIENT_ID)
                        .setClientSecret(CLIENT_SECRET)
                        .setRedirectUris(List.of(REDIRECT_URI)));

        return new GoogleAuthorizationCodeFlow.Builder(
                GoogleNetHttpTransport.newTrustedTransport(),
                JSON_FACTORY,
                clientSecrets,
                SCOPES
        ).setAccessType("offline").build();
    }

    public static String getGoogleUserEmail(String authCode) {
        try {
            GoogleAuthorizationCodeFlow flow = getGoogleAuthFlow();
            GoogleTokenResponse tokenResponse = flow.newTokenRequest(authCode)
                    .setRedirectUri(REDIRECT_URI)
                    .execute();
            Credential credential = flow.createAndStoreCredential(tokenResponse, null);

            Oauth2 oauth2 = new Oauth2.Builder(
                    GoogleNetHttpTransport.newTrustedTransport(),
                    JSON_FACTORY,
                    credential
            ).setApplicationName("VifinanceNews").build();

            Userinfo userInfo = oauth2.userinfo().get().execute();
            return userInfo.getEmail();
        } catch (IOException | GeneralSecurityException e) {
            e.printStackTrace();
            return null;
        }
    }
}
