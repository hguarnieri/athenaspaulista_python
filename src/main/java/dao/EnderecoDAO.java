package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

import models.Endereco;
import models.Linha;
import utils.MySqlConnection;

/**
 * Created by Henrique on 2/04/2016.
 * TODO use MongoDB
 */
public class EnderecoDAO
{
	public List<Endereco> getEnderecos(String linha, int idaVolta)
	{
		List<Endereco> enderecos = new ArrayList<>();
		
		try (Connection con = MySqlConnection.getConnection())
		{
			String sql = "SELECT Linha, Ordem, Endereco, IdaVolta\n" + "FROM Athenas.Enderecos\n" + "WHERE linha = ? AND IdaVolta = ?\n";
			
			if (idaVolta == 1)
			{
				sql += "ORDER BY Ordem";
			}
			else if (idaVolta == 2)
			{
				sql += "ORDER BY Ordem DESC";
			}
			
			PreparedStatement p = con.prepareStatement(sql);
			p.setString(1, linha);
			p.setInt(2, idaVolta);
			
			ResultSet rs = p.executeQuery();
			while (rs.next())
			{
				Endereco endereco = new Endereco();
				
				endereco.setLinha(rs.getString("linha"));
				endereco.setEndereco(rs.getString("endereco"));
				endereco.setIdavolta(rs.getInt("idaVolta"));
				endereco.setOrdem(rs.getInt("ordem"));
				
				enderecos.add(endereco);
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		
		return enderecos;
	}
	
	public Linha getLinha(String id)
	{
		Linha linha = new Linha();
		
		try (Connection con = MySqlConnection.getConnection())
		{
			String sql = "SELECT DISTINCT Numero, Descricao, Link, horarioIda, horarioVolta\n" + "FROM Athenas.linhas\n" + "WHERE Numero = ?";
			
			PreparedStatement p = con.prepareStatement(sql);
			p.setString(1, id);
			
			ResultSet rs = p.executeQuery();
			while (rs.next())
			{
				linha.setNumero(rs.getString("numero"));
				linha.setNome(rs.getString("descricao"));
				linha.setLink(rs.getString("link"));
				linha.setHorarioIda(rs.getString("horarioIda"));
				linha.setHorarioVolta(rs.getString("horarioVolta"));
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		
		return linha;
	}
}
