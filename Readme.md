# Crypto Arbitrage Tracker  
_Autor: Gabriela Rodríguez_  

## 🚀 Overview  
Sistema automatizado para detectar oportunidades de arbitraje en criptomonedas (Binance P2P vs. mercados locales como El Dorado).  

## 📊 Features  
- **Extracción de datos:** Web scraping/APIs (Binance, El Dorado).  
- **Cálculo de spreads:** Pandas + Python.  
- **Dashboard:** Power BI con historial y alertas.  
- **Automatización:** Despliegue en DigitalOcean con CI/CD.  

## 🛠️ Tech Stack  
| Área          | Tecnologías                                                                 |  
|---------------|-----------------------------------------------------------------------------|  
| Backend       | Python (Pandas, Flask), APIs REST                                           |  
| Data Pipeline | Airflow, Cron (para scheduling)                                             |  
| Cloud         | DigitalOcean (Droplet + Spaces S3), Docker                                  |  
| DevOps        | GitHub Actions (CI/CD), Grafana (monitoreo), Terraform (IaC)                |  
| Visualización | Power BI (+ Power Automate para notificaciones)                             |  

## 📈 Arquitectura  
```mermaid  
graph LR  
A[Binance API/Scraping] --> B(Python ETL)  
C[El Dorado Scraping] --> B  
B --> D{Data Processing}  
D --> E[(DigitalOcean Spaces S3)]  
E --> F[Power BI Dashboard]  
D --> G[Alertas vía Telegram]  