from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "qdrant"

class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"