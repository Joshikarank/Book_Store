from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    superkey: str
    jwt_key: str
    jwt_algo: str
    
    secret_key: str
    mail_server: str
    mail_port: int  
    mail_username: str
    mail_password: str
    base_url: str

settings = Settings()