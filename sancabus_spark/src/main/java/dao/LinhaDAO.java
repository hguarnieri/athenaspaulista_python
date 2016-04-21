package dao;

import models.Linha;
import utils.MySqlConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Henrique on 2/04/2016.
 */
public class LinhaDAO {

    Connection conn = null;
    Statement stmt = null;

    public List<Linha> getLinhas(String parametro1, String parametro2) {
        List<Linha> linhas = new ArrayList();

        if (parametro1.equals("all")) {
            parametro1 = "";
        }

        if (parametro2.equals("all")) {
            parametro2 = "";
        }

        try {

            conn = MySqlConnection.getConnection();

            String sql = "SELECT DISTINCT Numero, Descricao, Link, horarioIda, horarioVolta FROM athenas.linhas\n" +
                    "LEFT JOIN Athenas.enderecos ON linha = numero\n" +
                    "WHERE endereco IS NOT NULL \n" +
                    "AND UPPER(endereco) LIKE UPPER(?) \n" +
                    "AND Numero IN (SELECT DISTINCT linha FROM enderecos WHERE endereco LIKE UPPER(?))";

            PreparedStatement p = conn.prepareStatement(sql);
            p.setString(1, "%" + parametro1 + "%");
            p.setString(2, "%" + parametro2 + "%");

            ResultSet rs = p.executeQuery();
            while (rs.next()) {
                Linha linha = new Linha();

                linha.setNumero(rs.getString("numero"));
                linha.setNome(rs.getString("descricao"));
                linha.setLink(rs.getString("link"));
                linha.setHorarioIda(rs.getString("horarioIda"));
                linha.setHorarioVolta(rs.getString("horarioVolta"));

                linhas.add(linha);
            }
        } catch (SQLException se) {
            se.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (stmt != null)
                    stmt.close();
            } catch (SQLException se2) {

            }
            try {
                if (conn != null)
                    conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }

        return linhas;
    }

    public Linha getLinha(String id) {
        Linha linha = new Linha();

        EnderecoDAO enderecoDAO = new EnderecoDAO();

        try {
            conn = MySqlConnection.getConnection();

            String sql = "SELECT DISTINCT Numero, Descricao, Link, horarioIda, horarioVolta\n" +
                            "FROM Athenas.linhas\n" +
                            "WHERE Numero = ?";

            PreparedStatement p = conn.prepareStatement(sql);
            p.setString(1, id);

            ResultSet rs = p.executeQuery();
            while (rs.next()) {
                linha.setNumero(rs.getString("numero"));
                linha.setNome(rs.getString("descricao"));
                linha.setLink(rs.getString("link"));
                linha.setHorarioIda(rs.getString("horarioIda"));
                linha.setHorarioVolta(rs.getString("horarioVolta"));
            }

            linha.setEnderecosIda(enderecoDAO.getEnderecos(linha.getNumero(), 1));
            linha.setEnderecosVolta(enderecoDAO.getEnderecos(linha.getNumero(), 2));
        } catch (SQLException se) {
            se.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (stmt != null)
                    stmt.close();
            } catch (SQLException se2) {

            }
            try {
                if (conn != null)
                    conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }

        return linha;
    }
}
