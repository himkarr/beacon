from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Gemini (commented out — use Grok / xAI instead) ---
    # gemini_api_key: str
    # gemini_model: str = "gemini-2.0-flash"

    # --- Groq (free tier, Llama / Mixtral / DeepSeek) ---
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    groq_max_tokens: int = 8192


settings = Settings()