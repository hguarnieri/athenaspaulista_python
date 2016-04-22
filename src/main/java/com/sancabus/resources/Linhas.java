package com.sancabus.resources;

import static com.mongodb.client.model.Filters.eq;
import static spark.Spark.get;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.JsonArray;
import com.mongodb.BasicDBList;
import com.mongodb.BasicDBObject;
import com.mongodb.Block;
import com.mongodb.client.FindIterable;
import com.sancabus.db.MongoManager;

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
		
		Document routes = MongoManager.getRoutes().find(eq("number", id)).first();
		
		if (routes == null)
		{
			return null;
		}
		
		return routes.toJson();
	}
	
	private String getLinhaFull(Request request, Response response)
	{
		String from = request.splat()[0];
		String to = request.splat()[1];
		log.info("Requested from " + from + " to " + to);
		
		BasicDBObject regexFrom = new BasicDBObject("$regex", "(?i)(.*" + from + ".*)"); // LIKE % from %
		BasicDBObject regexTo = new BasicDBObject("$regex", "(?i)(.*" + to + ".*)"); // LIKE % to %
		
		// has FROM and TO with type 1
		BasicDBList and = new BasicDBList();
		and.add(new BasicDBObject("addressesToGo", new BasicDBObject("$elemMatch", new BasicDBObject("address", regexFrom))));
		and.add(new BasicDBObject("addressesToGo", new BasicDBObject("$elemMatch", new BasicDBObject("address", regexTo))));
		
		// has FROM and TO with type 2
		BasicDBList and2 = new BasicDBList();
		and2.add(new BasicDBObject("addressesToGoBack", new BasicDBObject("$elemMatch", new BasicDBObject("address", regexFrom))));
		and2.add(new BasicDBObject("addressesToGoBack", new BasicDBObject("$elemMatch", new BasicDBObject("address", regexTo))));
		
		// type1 OR type2
		BasicDBList or = new BasicDBList();
		or.add(new BasicDBObject("$and", and));
		or.add(new BasicDBObject("$and", and2));
		
		FindIterable<Document> iterable = MongoManager.getRoutes().find(new BasicDBObject("$or", or));
		
		JsonArray arr = new JsonArray();
		iterable.forEach((Block<Document>) res -> arr.add(res.toJson()));
		
		return arr.toString();
	}
}
