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
│   ├── compose.yaml # Configuración de servicios Docker
│   └── .env                  # Variables de entorno
├── extended/
│   └── sale_extended/
│       ├── models/
│       │   └── integration_order.py #Modelo integración
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
