package utils;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.SQLException;

public class MySqlConnection {
    private static String dbUrl = "jdbc:mysql://localhost:3306/athenas";
    private static String dbUsername = "webserver";
    private static String dbPassword = "athenas123";

    static HikariConfig config;

    static HikariDataSource ds;

    public static Connection getConnection() throws SQLException {
        if (config == null) {
            config = new HikariConfig();
            config.setJdbcUrl(dbUrl);
            config.setUsername(dbUsername);
            config.setPassword(dbPassword);
            config.addDataSourceProperty("cachePrepStmts", "true");
            config.addDataSourceProperty("prepStmtCacheSize", "250");
            config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");

            ds = new HikariDataSource(config);
        }

        return ds.getConnection();
    }
}