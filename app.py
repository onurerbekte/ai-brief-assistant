"""Kurgusal demo proje / Fictional demo project: AI brief assistant."""
import os
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator
from service import BriefService, BriefError


class BriefInput(BaseModel):
    model_config=ConfigDict(extra="forbid")
    brief:str=Field(min_length=10,max_length=6000)
    language:Literal["tr","en"]="tr"

    @field_validator("brief")
    @classmethod
    def not_blank(cls,value):
        value=value.strip()
        if len(value)<10:raise ValueError("Brief too short / Brief çok kısa")
        return value


def create_app(service=None):
    service=service or BriefService(mode=os.getenv("BRIEF_MODE","demo"))
    app=FastAPI(title="Brief Assistant / Brief Asistanı")
    assets=Path(__file__).parent/"static"
    app.mount("/static",StaticFiles(directory=assets),name="static")

    @app.get("/")
    def index():return FileResponse(assets/"index.html")

    @app.get("/health")
    def health():return {"status":"ok","mode":service.mode}

    @app.post("/brief")
    def brief(payload:BriefInput):
        try:
            return {"text":service.generate(payload.brief,payload.language),"mode":service.mode,"language":payload.language}
        except BriefError as exc:
            raise HTTPException(exc.status,str(exc)) from None
    return app


app=create_app()
