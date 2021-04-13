from db import database

@database.transaction()
async def create_user(email: str, password: str, first_name: str, last_name): 
    async with database.connect(): 
        result = database.fetch_one(
            query="""
                CALL create_user(:token, :email, :password, :first_name, :last_name)
            """, 
            value={
                "token": "Test123", 
                "email": email, 
                "password": password, 
                "first_name": first_name, 
                "last_name": last_name
            }
        )