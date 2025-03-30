from pymongo import MongoClient

def fetch_jobs_from_db(uri, db_name, collection_name):
    """
    Connects to a MongoDB database, retrieves job titles and descriptions,
    and converts the data into a dictionary.

    Args:
        uri (str): The MongoDB connection URI.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection containing job data.

    Returns:
        dict: A dictionary where keys are job titles and values are job descriptions.
    """
    # Connect to the MongoDB database
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # Fetch all documents from the collection
    jobs_cursor = collection.find()

    # Convert the data into a dictionary
    jobs_dict = {job["title"]: job["description"] for job in jobs_cursor}

    # Close the connection
    client.close()

    return jobs_dict