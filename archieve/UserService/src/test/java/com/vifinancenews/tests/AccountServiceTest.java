/*package com.vifinancenews.tests;

import com.vifinancenews.user.services.AccountService;

import com.vifinancenews.common.daos.AccountDAO;
import com.vifinancenews.common.daos.IdentifierDAO;
import com.vifinancenews.common.models.Account;
import com.vifinancenews.common.models.Identifier;
import com.vifinancenews.common.utilities.RedisCacheService;
import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;

import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyMap;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

class AccountServiceTest {

    private AccountService accountService;
    private UUID userId;
    private Account account;

    @BeforeEach
    void setUp() {
        accountService = new AccountService();
        userId = UUID.randomUUID();
        account = new Account(userId.toString(), "testUser", "avatar.png", "bio text");
    }

    @Test
    void testGetUserProfile_Cached() throws SQLException {
        try (MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class)) {
            Map<String, Object> cachedData = Map.of(
                "userId", userId.toString(),
                "userName", "cachedUser",
                "avatarLink", "avatar_cached.png",
                "bio", "cached bio"
            );
            redisMock.when(() -> RedisCacheService.getCachedUserData(userId.toString()))
                     .thenReturn(cachedData);

            Account result = accountService.getUserProfile(userId);
            assertEquals("cachedUser", result.getUserName());
        }
    }

    @Test
    void testGetUserProfile_FromDB() throws SQLException {
        try (MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class);
             MockedStatic<AccountDAO> daoMock = mockStatic(AccountDAO.class)) {

            redisMock.when(() -> RedisCacheService.getCachedUserData(userId.toString()))
                     .thenReturn(null);
            daoMock.when(() -> AccountDAO.getAccountByUserId(userId))
                   .thenReturn(account);

            Account result = accountService.getUserProfile(userId);
            assertEquals(account.getUserName(), result.getUserName());

            redisMock.verify(() -> RedisCacheService.cacheUserData(eq(userId.toString()), anyMap()));
        }
    }

    @Test
    void testUpdateUserProfile() throws SQLException {
        try (MockedStatic<AccountDAO> daoMock = mockStatic(AccountDAO.class);
             MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class)) {

            daoMock.when(() -> AccountDAO.updateAccount(userId, "newName", "newAvatar", "newBio"))
                   .thenReturn(true);
            daoMock.when(() -> AccountDAO.getAccountByUserId(userId))
                   .thenReturn(account);

            boolean result = accountService.updateUserProfile(userId, "newName", "newAvatar", "newBio");
            assertTrue(result);

            redisMock.verify(() -> RedisCacheService.clearUserData(userId.toString()));
            redisMock.verify(() -> RedisCacheService.cacheUserData(eq(userId.toString()), anyMap()));
        }
    }

    @Test
    void testSoftDeleteUserById() throws SQLException {
        try (MockedStatic<AccountDAO> daoMock = mockStatic(AccountDAO.class);
             MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class)) {

            daoMock.when(() -> AccountDAO.moveAccountToDeleted(userId)).thenReturn(true);

            boolean result = accountService.softDeleteUserById(userId);
            assertTrue(result);
            redisMock.verify(() -> RedisCacheService.clearUserData(userId.toString()));
        }
    }

    @Test
    void testDeleteUserByEmail_Success() throws SQLException {
        String email = "user@example.com";
        Identifier identifier = new Identifier(
    userId,
    email,
    "password_hash",
    "local",                          // loginMethod
    LocalDateTime.now(),              // createdAt
    LocalDateTime.now(),              // lastLogin
    0,                                // failedAttempts
    null                              // lockoutUntil
);

        try (MockedStatic<IdentifierDAO> idDao = mockStatic(IdentifierDAO.class);
             MockedStatic<AccountDAO> accDao = mockStatic(AccountDAO.class);
             MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class)) {

            idDao.when(() -> IdentifierDAO.getIdentifierByEmail(email)).thenReturn(identifier);
            accDao.when(() -> AccountDAO.deleteAccountByUserId(userId)).thenReturn(true);
            idDao.when(() -> IdentifierDAO.deleteIdentifierByEmail(email)).thenReturn(true);

            boolean result = accountService.deleteUserByEmail(email);
            assertTrue(result);
            redisMock.verify(() -> RedisCacheService.clearUserData(userId.toString()));
        }
    }

    @Test
    void testDeleteUserById_FromDeletedAccounts() throws SQLException {
        try (MockedStatic<AccountDAO> accDao = mockStatic(AccountDAO.class);
             MockedStatic<IdentifierDAO> idDao = mockStatic(IdentifierDAO.class);
             MockedStatic<RedisCacheService> redisMock = mockStatic(RedisCacheService.class)) {

            accDao.when(() -> AccountDAO.deleteAccountByUserId(userId)).thenReturn(false);
            accDao.when(() -> AccountDAO.deleteFromDeletedAccounts(userId)).thenReturn(true);
            idDao.when(() -> IdentifierDAO.deleteIdentifierByUserId(userId)).thenReturn(true);

            boolean result = accountService.deleteUserById(userId);
            assertTrue(result);
            redisMock.verify(() -> RedisCacheService.clearUserData(userId.toString()));
        }
    }

    @Test
    void testPermanentlyDeleteExpiredAccounts() throws SQLException {
        try (MockedStatic<AccountDAO> accDao = mockStatic(AccountDAO.class);
             MockedStatic<IdentifierDAO> idDao = mockStatic(IdentifierDAO.class)) {

            idDao.when(() -> IdentifierDAO.deleteExpiredIdentifiers(30)).thenReturn(true);
            accDao.when(() -> AccountDAO.deleteExpiredDeletedAccounts(30)).thenReturn(false);

            boolean result = AccountService.permanentlyDeleteExpiredAccounts(30);
            assertTrue(result);
        }
    }
}
*/