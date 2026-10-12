from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    server: ServerConfig
    directory: Path


class ServerConfig(BaseModel):
    host: str
    port: int
