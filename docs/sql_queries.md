# Consultas SQL

las siguientes consultas presentan información relevante con respecto a los registros que evidencia el modelo de integración api

## Ordenes con pedidos 

```sql
SELECT
    iso.name AS order_sequence,
    iso.external_order_id AS external_id,
    rp.name AS customer,
    rp.vat AS customer_vat,
    so.name AS sale,
    so.amount_total AS amount_total,
    iso.state AS integration_state,
    iso.processed_at AS integration_date

FROM integration_sale_order AS iso
    INNER JOIN sale_order AS so ON so.id = iso.sale_id
    INNER JOIN res_partner AS rp ON rp.id = so.partner_id;

```

## Ordenes pendientes por procesar

```sql
SELECT
    iso.name AS order_sequence,
    iso.external_order_id AS external_id,
    rp.name AS customer,
    rp.vat AS customer_vat,
    so.name AS sale,
    iso.state AS integration_state,
    iso.processed_at AS integration_date

FROM integration_sale_order AS iso
    INNER JOIN sale_order AS so ON so.id = iso.sale_id
    INNER JOIN res_partner AS rp ON rp.id = so.partner_id;
WHERE
    iso.state = 'pending'

```

## Ordenes con recepción fallida

```sql
SELECT
    iso.name AS order_sequence,
    iso.external_order_id AS external_id,
    iso.error_message AS error,
    COUNT(il) AS logs_len

FROM integration_sale_order AS iso
    INNER JOIN integration_log AS il ON il.integration_sale_order_id = iso.id
WHERE
    iso.state = 'failed'
GROUP BY
    iso.name,
    iso.external_order_id,
    iso.error_message;
```

## Logs con errores

```sql
SELECT
    iso.name AS order_sequence,
    iso.external_order_id AS external_id,
    il.level AS level,
    il.message AS message
FROM integration_log AS il
    INNER JOIN integration_sale_order AS iso ON il.integration_sale_order_id = iso.id
WHERE
    il.level = 'info'
```


## Orden que no contiene ciertos productos y su pedido fue cambiado a venta

```sql
SELECT
    iso.name AS order_sequence,
    iso.external_order_id AS external_id
FROM integration_sale_order AS iso
    INNER JOIN sale_order AS so ON so.id = iso.sale_id
    INNER JOIN sale_order_line AS sol ON sol.order_id = iso.id
    INNER JOIN product_product AS pp ON pp.id = sol.product_id
    INNER JOIN res_partner AS rp ON rp.id = so.partner_id
WHERE
    pp.default_code NOT IN ('sa003', 'sa004')
    AND so.state = 'sale'
GROUP BY
    iso.name,
    iso.external_order_id;
```