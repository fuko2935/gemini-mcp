import os
import logging
from dotenv import load_dotenv
import google.generativeai as gemini
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Sadece console output
    ]
)
logger = logging.getLogger(__name__)

from tools import prepare_full_context

# .env dosyasını yükle ve Gemini client'ını başlat
load_dotenv()
gemini.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Sabit sistem promptu
SYSTEM_PROMPT = """
Sen bir yazılım geliştirici asistanısın. Görevin şu kurallara uyarak yardım etmek:

## Proje Rolü:
- Kod analizi ve geliştirme konularında uzman destek sağlama
- Proje bağlamını dikkate alarak öneriler sunma
- Teknik sorunları çözme ve iyileştirme önerileri verme

## Kurallar:
1. Her zaman Türkçe yanıt ver
2. Kod örnekleri net ve anlaşılır olmalı
3. Proje dosyalarını ve yapısını analiz ederek bağlama uygun öneriler sun
4. Güvenlik ve performans konularını göz önünde bulundur
5. Best practice'leri uygula

## Çıktı Formatı:
- Açıklayıcı başlıklar kullan
- Kod blokları için uygun syntax highlighting
- Adım adım açıklamalar ver
- Gerekirse örnek kullanım senaryoları ekle
- Önemli noktaları vurgula

## Bağlam:
Kullanıcının sorusu ve proje dosyalarının içeriği aşağıda verilmiştir. Bu bilgileri kullanarak kapsamlı ve yararlı bir yanıt hazırla.
"""

# FastAPI uygulamasını oluştur
app = FastAPI(title="Gemini MCP Server", description="Gemini AI ile MCP sunucusu")

# Middleware - API anahtarı doğrulaması
async def verify_api_key(request: Request):
    api_key = request.headers.get('X-Mcp-Api-Key')
    if not api_key:
        raise HTTPException(status_code=403, detail="API anahtarı gerekli")
    # Burada API anahtarını doğrulama mantığını ekleyebilirsiniz
    return api_key

# Request modeli
class GenerateRequest(BaseModel):
    prompt: str

# Response modeli
class GenerateResponse(BaseModel):
    response: str
    status: str = "success"

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "gemini-mcp-server"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, api_key: str = Depends(verify_api_key)):
    try:
        # Proje bağlamını hazırla
        full_context = prepare_full_context()
        
        # Sistem promptu + kullanıcı promptu + proje bağlamı olarak content oluştur
        content = f"""{SYSTEM_PROMPT}

## Kullanıcı Sorusu:
{request.prompt}

## Proje Bağlamı:
{full_context}"""
        
        # Gemini modeli oluştur
        model = gemini.GenerativeModel('gemini-2.5-pro')
        
        # Gemini'den yanıt al (content listesi olarak gönder)
        response = model.generate_content([content])
        
        # HTTP 200 ile yanıt döndür
        return GenerateResponse(
            response=response.text,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")

# Sunucuyu çalıştır
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
