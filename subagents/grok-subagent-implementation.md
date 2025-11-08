# Grok Sub-agent Implementation with Pydantic

This document outlines the recommended approach for implementing a Grok sub-agent for Claude Code, using Pydantic for configuration management.

## API Key Management with Pydantic

To handle the Gemini API key securely and efficiently, we will use Pydantic's `BaseSettings` model. This approach allows us to define a clear configuration schema and automatically load the API key from environment variables or a `.env` file.

### 1. Define the Settings Model

First, create a `Settings` class that inherits from `pydantic_settings.BaseSettings`. This class will define the fields required for the sub-agent's configuration.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Defines the configuration settings for the Grok sub-agent.
    """
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")

```

### 2. Environment Variable

The `gemini_api_key` is expected to be stored in a `.env` file in the project's root directory. The entry in the `.env` file should look like this:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 3. Usage

To access the API key, simply instantiate the `Settings` model:

```python
# Load the settings
settings = Settings()

# Access the API key
api_key = settings.gemini_api_key

# Use the API key to configure the Gemini client
# (example using google-genai)
# import google.generativeai as genai
# genai.configure(api_key=api_key)
```

This approach ensures that the API key is not hard-coded and can be easily managed in different environments (development, testing, production) by using different `.env` files or environment variables.
