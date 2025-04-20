# 🧠 Diseño de Producto

El diseño de producto es el proceso de definir **qué problema se va a resolver, para quién y cómo se resolverá**. Abarca desde la idea inicial hasta cómo se ve y se usa el producto. En este proyecto, lo aplicamos así:

## ✅ Problema detectado

Muchos traders de P2P pierden oportunidades por no tener herramientas de análisis ni alertas automáticas. El mercado P2P carece de soluciones que automaticen el monitoreo de precios y el análisis del spread, lo que genera pérdida de tiempo y oportunidades.

## 💡 Propuesta de Valor

> "Este sistema automatiza el monitoreo y alerta de oportunidades reales de arbitraje en el mercado P2P, ahorrando tiempo y mejorando la rentabilidad para traders que no cuentan con herramientas profesionales."

## 🧭 Público objetivo

- Traders P2P activos (novatos o intermedios)
- Freelancers que hacen arbitraje ocasional
- Personas con conocimientos básicos en cripto y banca digital
- Usuarios que operan en Binance P2P y plataformas locales como El Dorado

## 🧩 Diferenciadores

- Automatización E2E (extracción, cálculo, alertas)
- Visualización clara de tendencias y márgenes
- Despliegue ligero (DigitalOcean + Docker)
- Enfoque en mercados LATAM con monedas inestables (ej. VES)

---

# 🚧 Roadmap

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Roadmap: Crypto Arbitrage Tracker

    section Etapa 1: Base técnica
    Infraestructura IaC (Terraform + DO)        :a1, 2025-04-20, 4d
    Extracción de datos Binance y ElDorado       :a2, after a1, 4d
    Cálculo de spreads y validaciones            :a3, after a2, 4d
    Test unitarios y de integración              :a4, after a3, 3d

    section Etapa 2: Automatización
    Scheduling con Cron                          :b1, after a4, 2d
    Configuración de alertas Telegram/Email      :b2, after b1, 3d
    Dockerización y CI/CD con Jenkins            :b3, after b2, 3d

    section Etapa 3: Visualización + Feedback
    Almacenamiento de históricos en S3           :c1, after b3, 2d
    Dashboard Power BI + conexión a S3           :c2, after c1, 4d
    Landing Page + Captación de correos          :c3, after c2, 3d

    section Etapa 4: Validación
    Pruebas con usuarios y feedback              :d1, after c3, 5d
    Iteraciones según feedback                   :d2, after d1, 5d

    section Etapa 5: Escalabilidad (futuro)
    Separación por microservicios                :e1, after d2, 5d
    Soporte para más monedas y mercados          :e2, after e1, 5d
