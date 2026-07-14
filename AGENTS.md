# AGENTS.md

## Propósito del proyecto
Integración entre un sistema externo de pedidos y Odoo, mediante una API REST que recibe órdenes, valida cliente/productos, crea órdenes de venta y registra trazabilidad de cada intento de integración.

## Stack técnico
- Odoo 19.0 (Community)
- PostgreSQL 15
- Docker / Docker Compose
- Python (controladores HTTP nativos de Odoo, sin frameworks externos)
- Swagger/OpenAPI 3.0 para documentación de API

## Estructura del repositorio
- `extended/sale_extended/` — módulo custom de Odoo
  - `controllers/` — endpoints REST (`/api/v1/orders`, `/api/v1/products`)
  - `models/integration_sale_order.py` — modelo de trazabilidad de integración
  - `security/` — reglas de acceso y grupos
- `docker/` — `docker-compose.yml`, configuración de Odoo/Postgres
- `docs/swagger.yaml` — especificación OpenAPI de la API
- `docs/sql_queries.md` — consultas SQL de análisis sobre datos de integración
- `docs/diagram/` — diagrama lógico y de relación de datos

## Convenciones de código
- Nombres de variables/funciones en inglés.
- Validaciones separadas en métodos privados (`_validate_*`) dentro del
  controlador, cada una retornando `None` si pasa, o una respuesta de error.
- Respuestas HTTP estandarizadas vía `_send_response(status, success, code, message, **extra)`.
- Autenticación: Bearer token estático validado en `auth='bearer'`
  (ver `API_KEY` en `order_api.py` — pendiente de mover a `ir.config_parameter`
  antes de producción).

## Cómo ejecutar el proyecto
```bash
cd docker
docker compose up -d odoo -i sale_extended
```

## Cómo actualizar el módulo tras cambios
```bash
docker compose run --rm web odoo -d odoo -u sale_extended --stop-after-init
```

## Decisiones de arquitectura relevantes
- El healthcheck de `db` (`pg_isready`) evita condiciones de carrera al
  levantar `web` antes de que Postgres esté listo.
- CORS abierto (`cors='*'`) es aceptable aquí porque la autenticación es por apikey en header, no por cookie de sesión (sin riesgo de CSRF).

## Cómo debe comportarse un agente de IA trabajando en este repo
- Mantener el patrón `_validate_*` → retorna `None` o respuesta de error,
  no lanzar excepciones genéricas.
- Toda nueva ruta debe documentarse en `docs/swagger.yaml` siguiendo los
  schemas ya definidos (`ErrorResponse`, patrón `_send_response`).