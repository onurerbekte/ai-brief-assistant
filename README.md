# Brief Studio — AI brief asistanı / AI brief assistant
**Kurgusal demo proje / Fictional demo project.**

## Türkçe
FastAPI arayüzü ve OpenAI Responses API entegrasyonu. Brief metninden teslimler, açık sorular, riskler ve sonraki adım taslağı üretir. Varsayılan **demo** modu yerel şablondur; AI çalıştığı iddia edilmez ve anahtar gerekmez. Türkçe/İngilizce arayüz.

Python 3.12+ sanal ortamında `python -m pip install -r requirements.txt`, ardından:
```powershell
python -m pytest -q
python -m uvicorn app:app --host 127.0.0.1 --port 8001
```
`http://127.0.0.1:8001` aç. Brief en az 10, en fazla 6000 karakter. Çıktı tarayıcıda görünür; kalıcı kaydedilmez. Ctrl+C ile durdur.

Canlı mod için `BRIEF_MODE=live`, `OPENAI_API_KEY` ve erişebildiğin model adı olarak `OPENAI_MODEL` ortam değişkenlerini **kendi terminalinde** ayarla. Gerçek anahtar `.env.example` veya kaynak koda yazılmaz. `.env` otomatik yüklenmez. Anahtar yalnızca sunucuda kalır; tarayıcıya gönderilmez. Canlı mod kullanıcının briefini OpenAI'a iletir ve API kullanım maliyeti doğurabilir; bu projede gerçek API isteği yapılmadı. API timeout 30 saniye, tekrar deneme kapalı, `store=False`, çıktı sınırı 1200 token. Yerel demo; kimlik doğrulama yok ve public sunucu olarak yayınlanmadı.

## English
A FastAPI interface integrated with the OpenAI Responses API to organize project briefs into deliverables, questions, risks, and next steps. Default **demo** mode returns a local template with no AI request or key required. Bilingual UI.

Install requirements in a Python 3.12+ virtual environment and run the commands above. Open port 8001. Inputs accept 10–6000 characters; results are displayed without persistent storage. Stop with Ctrl+C.

For live mode, set `BRIEF_MODE=live`, `OPENAI_API_KEY`, and an accessible model name in `OPENAI_MODEL` in your own terminal. No automatic dotenv loading. Never commit real keys; they remain server-side. Live mode sends your brief to OpenAI and may incur API costs. No live request was made for this project. Timeout 30 seconds, no automatic retries, `store=False`, and a 1200-token output cap. This is a local demo without authentication or public deployment.

## Resmi kaynak / Official source
Responses API: https://developers.openai.com/api/reference/python/resources/responses/methods/create
