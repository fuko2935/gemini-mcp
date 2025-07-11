# Gemini MCP Server

Gemini AI ile MCP (Model Context Protocol) sunucusu.

## Özellikler

- **Sistem Promptu Entegrasyonu**: Sabit sistem promptu ile proje rolü, kurallar ve çıktı formatı tanımlamaları
- **Proje Bağlamı Analizi**: Proje dosyalarının otomatik analizi ve bağlam oluşturma
- **FastAPI Tabanlı**: RESTful API ile erişim
- **Güvenlik**: API anahtarı doğrulaması

## Sistem Promptu Yapısı

Sistem promptu aşağıdaki bileşenleri içerir:

1. **Proje Rolü**: Yazılım geliştirici asistanı olarak rol tanımı
2. **Kurallar**: 
   - Türkçe yanıt verme
   - Net kod örnekleri
   - Bağlama uygun öneriler
   - Güvenlik ve performans odaklı yaklaşım
   - Best practice uygulamaları

3. **Çıktı Formatı**:
   - Açıklayıcı başlıklar
   - Syntax highlighting
   - Adım adım açıklamalar
   - Örnek kullanım senaryoları
   - Vurgulamalar

## Prompt Yapısı

```
Sistem Promptu
+ 
Kullanıcı Sorusu
+ 
Proje Bağlamı
```

Bu yapı `model.generate_content([content])` ile Gemini API'sine gönderilir.

## Kullanım

1. `.env` dosyasında `GEMINI_API_KEY` tanımlayın
2. Sunucuyu başlatın: `python mcp_server.py`
3. POST isteği gönderin: `/generate` endpoint'ine
4. `X-Mcp-Api-Key` header'ı ile API anahtarınızı gönderin

## Geliştiriciler

- API anahtarı doğrulaması için `verify_api_key` fonksiyonu
- Proje bağlamı hazırlama için `prepare_full_context` fonksiyonu
- Sistem promptu `SYSTEM_PROMPT` sabiti olarak tanımlanmış

## Güncelleme Notları

### Step 5: Sistem Promptu Entegrasyonu ✅
- Sabit sistem promptu eklendi
- Proje rolü, kurallar ve çıktı formatı tanımlandı
- Content yapısı: kullanıcı promptu + sistem promptu + proje bağlamı
- `model.generate_content([content])` ile gönderim
