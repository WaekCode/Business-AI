from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname : str 
    database_port :str 
    database_password :str
    database_name: str 
    database_username : str
    
    model_config= {
        "env_file": ".env"
    }
   

settings = Settings()