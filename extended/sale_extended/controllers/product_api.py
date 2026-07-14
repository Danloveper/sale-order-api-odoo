from odoo import http
from odoo.http import request

class OrderApi(http.Controller):

    @http.route('/api/v1/products', auth='bearer', methods=['GET'], type='http', csrf=False, cors='*')
    def get_sale_products(self):

        products = request.env['product.product'].sudo().search_read(
            domain=[
                ('sale_ok', '=', True),
            ],
            fields=['default_code', 'name', 'description']
        )

        products_info = [
            {k: v for k, v in product.items() if k != 'id'}
            for product in products
        ]

        if not products:
            return self._send_response(
                200,
                True,
                'PRODUCTS_FOUND',
                '0 product(s) found.',
            )
        
        return self._send_response(
                200,
                True,
                'PRODUCTS_FOUND',
                f'{len(products_info)} product(s) found.',
                products=products_info
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
