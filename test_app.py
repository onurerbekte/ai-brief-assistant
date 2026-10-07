from types import SimpleNamespace
from unittest.mock import Mock
import httpx2
from fastapi.testclient import TestClient
from openai import APITimeoutError,RateLimitError
import pytest
from app import create_app
from service import BriefService


def test_demo_and_static_assets():
    with TestClient(create_app(BriefService())) as client:
        assert client.get("/").status_code==200
        assert client.get("/static/app.js").status_code==200
        assert client.get("/health").json()["mode"]=="demo"
        for language,marker in (("tr","DEMO ŞABLONU"),("en","DEMO TEMPLATE")):
            result=client.post("/brief",json={"brief":"A fictional café website","language":language})
            assert result.status_code==200 and marker in result.json()["text"]


@pytest.mark.parametrize("payload",[{"brief":"short"},{"brief":" "*20},{"brief":"x"*6001},{"brief":"Valid demo project","language":"de"}])
def test_input_validation(payload):
    with TestClient(create_app(BriefService())) as client:
        assert client.post("/brief",json=payload).status_code==422


def test_live_missing_config_is_explicit(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False);monkeypatch.delenv("OPENAI_MODEL",raising=False)
    with TestClient(create_app(BriefService(mode="live"))) as client:
        assert client.post("/brief",json={"brief":"A fictional café website"}).status_code==503


def test_mocked_responses_payload_and_output():
    fake=Mock();fake.responses.create.return_value=SimpleNamespace(output_text="  Scope\nDemo deliverables  ")
    with TestClient(create_app(BriefService(mode="live",client=fake,model="fictional-test-model"))) as client:
        response=client.post("/brief",json={"brief":"A fictional café website","language":"en"})
        assert response.json()["text"]=="Scope\nDemo deliverables"
    args=fake.responses.create.call_args.kwargs
    assert args["store"] is False and args["max_output_tokens"]==1200
    assert args["input"]=="A fictional café website" and "English" in args["instructions"]


@pytest.mark.parametrize("kind,status",[("rate",503),("timeout",504),("empty",502)])
def test_mocked_provider_failures(kind,status):
    fake=Mock();request=httpx2.Request("POST","https://example.test/responses")
    if kind=="rate":fake.responses.create.side_effect=RateLimitError("demo",response=httpx2.Response(429,request=request),body=None)
    elif kind=="timeout":fake.responses.create.side_effect=APITimeoutError(request=request)
    else:fake.responses.create.return_value=SimpleNamespace(output_text="")
    with TestClient(create_app(BriefService(mode="live",client=fake,model="fictional-test-model"))) as client:
        assert client.post("/brief",json={"brief":"A fictional café website"}).status_code==status
