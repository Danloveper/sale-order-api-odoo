# Sale Order API Odoo

API de integración para procesar órdenes de venta externas en Odoo 19.

## 📋 Descripción

Este proyecto implementa un módulo Odoo (`sale_extended`) que integra órdenes externas con el sistema de Odoo. Incluye un modelo `IntegrationOrder` para gestionar el procesamiento, validación y sincronización de órdenes desde sistemas externos.

## 🚀 Tecnologías

- **Odoo**: 19.0
- **PostgreSQL**: 15
- **Docker & Docker Compose**: Para orquestación
- **Python**: Backend de Odoo

## 📁 Estructura del Proyecto

```
odoo-19/
├── docker/
|   ├── config/
|   |   └── odoo.conf   # Configuración de servicio Odoo
|   |
│   ├── compose.yaml      # Configuración de servicios Docker
│   └── .env              # Variables de entorno
|
├── docs/                   
|   ├── diagrams/        # Diagrama Logico y E/R
|   |   ├── Diagram E_R - Sale API Odoo.png
|   |   └── Diagram Logic - Sale API Odoo.png
|   |
|   ├── sql_queries.md  # Consultas SQL Modelo Sale API
|   └── swagger.yaml    # Doc OpenAPI
|   
├── extended/
│   └── sale_extended/
|       ├── controllers/
|       |   ├── __init__.py
|       |   ├── order_api.py    # API para validar y crear Integración
|       |   └── product_api   # API para obtener productos vendibles
|       |
|       ├── data/
|       |   ├── integration_cron.xml # Acción Programada new partner/sale
|       |   └── ir.sequence.xml # Secuencia Model Integración
|       |
│       ├── models/
|       |   ├── __init__.py
│       │   └── integration_order.py # Modelo integración
|       |
|       ├── security/
|       |   └── ir.model.access.csv  #  Permisos Model Integración
|       |
|       ├── views/
|       |   └── integration_sale_order_views.xml  # Action, Menu, View
│       ├── __init__.py
│       └── __manifest__.py
|
└── README.md
```

## 🔧 Instalación y Configuración

### Requisitos Previos

- Docker y Docker Compose instalados
- Puerto 8069 disponible (Odoo)
- PostgreSQL accesible en el puerto 5432

### 1 . Setup del Entorno

```bash
# 1. Clonar/descargar este repositorio
# 2. Levantar el entorno
cd docker
docker-compose up -d -i sale_extended

# 3. Esperar a que los servicios inicien
```

Odoo estará disponible en `http://localhost:8069`



---

**Versión**: 1.0  
**Última actualización**: 2026-07-14
