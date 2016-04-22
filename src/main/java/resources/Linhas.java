package resources;

import static spark.Spark.get;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;

import dao.LinhaDAO;
import models.Linha;
import spark.Request;
import spark.Response;

public class Linhas implements IResource
{
	private final Logger log = LoggerFactory.getLogger(Linhas.class);
	
	@Override
	public void init()
	{
		get("/linhas/*/*", "application/json", (req, res) -> getLinhaFull(req, res));
		get("/linha/*", "application/json", (req, res) -> getLinha(req, res));
	}
	
	private String getLinha(Request request, Response response)
	{
		String id = request.splat()[0];
		log.info("Requested " + id);
		
		Gson gson = new Gson();
		LinhaDAO dao = new LinhaDAO();
		Linha linhas = dao.getLinha(id);
		return gson.toJson(linhas);
	}
	
	private String getLinhaFull(Request request, Response response)
	{
		String id = request.splat()[0];
		String to = request.splat()[1];
		log.info("Requested " + id + " to " + to);
		
		Gson gson = new Gson();
		LinhaDAO dao = new LinhaDAO();
		List<Linha> linhas = dao.getLinhas(id, to);
		return gson.toJson(linhas);
	}
}
