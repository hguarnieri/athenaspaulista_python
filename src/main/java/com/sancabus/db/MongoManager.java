package com.sancabus.db;

import org.bson.Document;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class MongoManager
{
	private final MongoClient mongoClient;
	private final MongoDatabase db;
	
	private MongoManager()
	{
		mongoClient = new MongoClient();
		db = mongoClient.getDatabase("sancabus");
	}
	
	public static MongoCollection<Document> getRoutes()
	{
		return getInstance().db.getCollection("routes");
	}
	
	public static MongoManager getInstance()
	{
		return SingletonHolder.instance;
	}
	
	private static class SingletonHolder
	{
		@SuppressWarnings("synthetic-access")
		protected static final MongoManager instance = new MongoManager();
	}
}
