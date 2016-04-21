import com.google.gson.Gson;
import dao.LinhaDAO;
import models.Endereco;
import models.Linha;
import spark.Spark;
import utils.MySqlConnection;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import static spark.Spark.*;

public class Main {
    public static void main(String[] args) {
        port(8080);

        //staticFileLocation("public");

        Spark.options("/*", (request, response)->{

            String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
            if (accessControlRequestHeaders != null) {
                response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
            }

            String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
            if(accessControlRequestMethod != null){
                response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
            }

            return "OK";
        });

        Spark.before((request,response)->{
            response.header("Access-Control-Allow-Origin", "*");
        });



        get("/hello", (req, res) -> "Hello World");

        get("/linhas/*/*", "application/json", (request, response) -> {
            Gson gson = new Gson();
            LinhaDAO dao = new LinhaDAO();
            List<Linha> linhas = dao.getLinhas(request.splat()[0], request.splat()[1]);
            return gson.toJson(linhas);
        });

        get("/linha/*", "application/json", (request, response) -> {
            Gson gson = new Gson();
            LinhaDAO dao = new LinhaDAO();
            Linha linhas = dao.getLinha(request.splat()[0]);
            return gson.toJson(linhas);
        });

    }
}