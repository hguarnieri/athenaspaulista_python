package com.sancabus;

import static spark.Spark.awaitInitialization;
import static spark.Spark.port;
import static spark.Spark.staticFileLocation;
import static spark.Spark.threadPool;

import org.reflections.Reflections;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.sancabus.resources.IResource;

public class Main
{
	private static final String PACKAGE = "com.sancabus.resources";
	private final Logger log = LoggerFactory.getLogger(Main.class);
	
	public static void main(String[] args)
	{
		new Main();
	}
	
	private Main()
	{
		port(8080);
		threadPool(8); // TODO config
		// secure(keystoreFile, keystorePassword, truststoreFile, truststorePassword);
		
		staticFileLocation("/sancabus");
		
		setupResources();
		
		awaitInitialization();
		
		/*
		 * Spark.options("/*", (request, response) ->
		 * {
		 * String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
		 * if (accessControlRequestHeaders != null)
		 * {
		 * response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
		 * }
		 * String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
		 * if (accessControlRequestMethod != null)
		 * {
		 * response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
		 * }
		 * return "OK";
		 * });
		 * Spark.before((request, response) ->
		 * {
		 * response.header("Access-Control-Allow-Origin", "*");
		 * });
		 */
	}
	
	private void setupResources()
	{
		int i = 0;
		for (Class<? extends IResource> res : new Reflections(PACKAGE).getSubTypesOf(IResource.class))
		{
			try
			{
				res.newInstance().init();
				i++;
			}
			catch (Exception e)
			{
				log.error("Bad resource at: " + res.getSimpleName());
				e.printStackTrace();
			}
		}
		
		log.info("Loaded " + i + " resource(s).");
	}
}