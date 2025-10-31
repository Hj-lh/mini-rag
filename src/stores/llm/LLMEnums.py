from enum import Enum

class LLMProvider(Enum):
    OLLAMA = "Ollama"
    OPENAI = "OpenAI"


class OllamaEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CohereEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"

