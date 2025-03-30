from pymongo import MongoClient

def update_jobs_in_db(uri, db_name, collection_name, jobs_dict):
    """
    Connects to a MongoDB database and updates it with job titles and descriptions
    from a given dictionary. If a job title already exists, its description is updated.
    Otherwise, a new document is inserted.

    Args:
        uri (str): The MongoDB connection URI.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection to update.
        jobs_dict (dict): A dictionary where keys are job titles and values are job descriptions.

    Returns:
        None
    """
    # Connect to the MongoDB database
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # Update or insert each job title and description
    for title, description in jobs_dict.items():
        collection.update_one(
            {"title": title},  # Match documents by job title
            {"$set": {"description": description}},  # Update the description
            upsert=True  # Insert the document if it doesn't exist
        )

    # Close the connection
    client.close()