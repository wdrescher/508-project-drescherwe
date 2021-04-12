from db import database

@database.transaction()
async def create_user(email: str, password: str, first_name: str, last_name): 
    async with database.connect(): 
        result = database.fetch_one(
            query="""
                INSERT INTO profile (email, password, first_name, last_name) VALUES ();
            """, 
            value=""
        )