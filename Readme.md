# Crypto Arbitrage Tracker  
*Autor: Gabriela Rodríguez*  

## 🚀 Overview  
Sistema automatizado para detectar oportunidades de arbitraje en criptomonedas entre Binance P2P y mercados locales como El Dorado. Implementa **Infraestructura como Código (IaC)** con Terraform para un despliegue reproducible en DigitalOcean.  

## 📊 Features  
- **Extracción de datos:** Web scraping/APIs (Binance, El Dorado) con manejo de errores  
- **Cálculo de spreads:** Pandas + Python con validación de datos  
- **Dashboard interactivo:** Power BI con visualización de tendencias históricas  
- **Automatización E2E:**  
  - CI/CD con GitHub Actions  
  - Orchestration con Terraform  
  - Scheduling con Cron/Airflow  

## 🛠️ Tech Stack  

| Área           | Tecnologías                                                                 |  
|----------------|-----------------------------------------------------------------------------|  
| **Backend**    | Python (Pandas, Flask), APIs REST, Type Hints                               |  
| **Data Pipe**  | Airflow, Cron, Validación de datos con Pydantic                            |  
| **Cloud**      | DigitalOcean (Droplet + Spaces S3), Docker, Terraform (IaC)                |  
| **DevOps**     | GitHub Actions (CI/CD), Grafana + Prometheus (monitoreo), Ansible (opcional)|  
| **Viz**        | Power BI (+ Power Automate), Alertas en Telegram/Email                      |  

## 📈 Arquitectura  

```mermaid  
graph TD  
    subgraph "Infraestructura (Terraform)"  
        A[DigitalOcean Droplet] --> B[Docker Engine]  
        C[DigitalOcean Spaces S3]  
    end  

    subgraph "Data Pipeline"  
        D[Binance API] -->|Requests| E[ETL Python]  
        F[El Dorado Scraping] --> E  
        E --> G{Procesamiento}  
        G -->|Datos limpios| C  
        G --> H[Alertas]  
    end  

    subgraph "Visualización"  
        C --> I[Power BI Dashboard]  
        H --> J[Telegram Bot]  
    end  