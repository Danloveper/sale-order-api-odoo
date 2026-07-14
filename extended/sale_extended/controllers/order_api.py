import json

from odoo import http
from odoo.http import request



API_KEY = '46369552636869cbb4a9a99ceeeef1e31822c80b'

class OrderApi(http.Controller):

    @http.route('/api/v1/orders', auth='bearer', methods=['POST'], type='http', csrf=False, cors='*')
    def create_order(self):
        payload = request.get_json_data()

        response = self._validate_response(payload)
        if response:
            return response
        
        customer = self._validate_customer(payload.get('customer'))
        if customer:
            return customer
        
        lines = self._validate_lines(payload.get('lines'))
        if lines:
            return lines
        
        integration_id = request.env['integration.sale.order'].sudo().create({
            'external_order_id': payload.get('external_order_id'),
            'payload':  payload,
        })
        integration_id.add_log('info', 'Order received successfully')

        return self._send_response(
            201,
            True,
            'ORDER_RECEIVED',
            'Order received successfully.',
            state=integration_id.state,
        )

    def _validate_response(self, payload):

        required_fields = [
            'external_order_id',
            'customer',
            'lines',
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in payload
        ]

        if missing_fields:
            return self._send_response(
                400,
                False,
                'MISSING_FIELDS',
                'Missing required fields.',
                fields=missing_fields,
            )

        if not isinstance(payload.get('customer'), dict):
            return self._send_response(
                400,
                False,
                'INVALID_FORMAT_CUSTOMER',
                'Customer must be an object.',
            )

        if not isinstance(payload.get('lines'), list):
            return self._send_response(
                400,
                False,
                'INVALID_LINES',
                'Lines must be an array.',
            )

        if not payload.get('lines'):
            return self._send_response(
                422,
                False,
                'EMPTY_ORDER',
                'The order must contain at least one line.',
            )
        
        order_duplicated = request.env['integration.sale.order'].sudo().search(
            domain=[
                ('external_order_id', '=', payload.get('external_order_id')),
            ],
            limit=1,  
        )
        
        if order_duplicated.exists():
            order_duplicated.add_log('warning', 'Duplicate order received.')
        
            return self._send_response(
                409,
                False,
                'DUPLICATED_ORDER',
                'The order already exists',
                external_order_id=order_duplicated.external_order_id,
                state=order_duplicated.state,
            )
        
        return None
        
    def _validate_customer(self, customer):
        customer_fields = ['is_company', 'vat', 'name', 'email', 'phone']
        customer_fields_missing = [
            field
            for field in customer_fields
            if field not in customer
        ]

        if customer_fields_missing:
            return self._send_response(
                400,
                False,
                'CUSTOMER_MISSING_FIELDS',
                'Fields are missing for the client.',
                fields=customer_fields_missing
            )
        
        return None
    
    def _validate_lines(self, lines):
        
        products_code = [line.get('default_code') for line in lines]
        products_odoo = request.env['product.product'].sudo().search_read(
            domain=[
                ('sale_ok', '=', True),
                ('default_code', 'in', products_code),
            ],
            fields=['default_code']
        )

        products_odoo_set = {
            product['default_code']
            for product in products_odoo
        }
        products_missing = [
            default_code
            for default_code in products_code
            if default_code not in products_odoo_set
        ]

        if products_missing:
            return self._send_response(
                422,
                False,
                'PRODUCTS_NOT_FOUND',
                'The products do not exist in Odoo.',
                products=products_missing,
            )

    
        invalid_quantities = [
            '%s: %s' % (line.get('default_code'), line.get('quantity') )
            for line in lines
            if not isinstance(line.get('quantity'), (int, float))
            or line.get('quantity') <= 0
        ]

        if invalid_quantities:
            return self._send_response(
                422,
                False,
                'QUANTITY_INVALID',
                'Some lines contain invalid quantities.',
                lines=invalid_quantities,
            )
        
        invalid_prices = [
            '%s: %s' % (line.get('default_code'), line.get('price') )
            for line in lines
            if not isinstance(line.get('price'), (int, float))
            or line.get('price') <= 0
        ]

        if invalid_prices:
            return self._send_response(
                422,
                False,
                'PRICE_INVALID',
                'Some lines contain invalid prices.',
                lines=invalid_prices,
            )
        
        products_map = {
            product['default_code']: product['id']
            for product in products_odoo
        }

        for line in lines:
            line.update({
                'product_id': products_map[line['default_code']]
            })

        return None
    
    @http.route('/api/v1/orders/<external_order_id>', auth='bearer', methods=['GET'], type='http', csrf=False, cors='*')
    def get_order_state(self, external_order_id: str):

        integration_id = request.env['integration.sale.order'].sudo().search(
            domain=[
                ('external_order_id', '=', external_order_id)
            ],
        )

        if integration_id:
            return self._send_response(
                200,
                True,
                'ORDER_FOUND',
                f'Order {integration_id.name} found.',
                state=integration_id.state,
                processed_date=integration_id.processed_at,
                sale=integration_id.sale_id.name or 'Without Quotation'
            )
        
        return self._send_response(
                404,
                False,
                'ORDER_NOT_FOUND',
                f'Order {external_order_id} not found.',
            )

    def _send_response(self, status, success, code, message, **extra):
        return request.make_json_response(
            status=status,
            data={
                'success': success,
                'code': code,
                'message': message,
                **extra,
            },
        )
    