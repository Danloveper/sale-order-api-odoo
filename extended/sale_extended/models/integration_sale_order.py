from odoo import _, api, fields, models


class IntegrationSaleOrder(models.Model):
    _name = 'integration.sale.order'
    _description = 'External Order Integration'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(
        required=True,
        default=lambda self: _('New'),
        readonly=True,
        copy=False,
    )

    external_order_id = fields.Char(
        required=True,
        index=True,
    )

    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('failed', 'Failed'),
        ],
        default='pending',
        required=True,
        tracking=True,
    )

    payload = fields.Json()

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        readonly=True,
    )

    processed_at = fields.Datetime(
        readonly=True,
    )

    error_message = fields.Text()

    log_ids = fields.One2many(
        comodel_name='integration.log',
        inverse_name='integration_sale_order_id',
    )

    _sql_constraints = [
        (
            'external_order_id_unique',
            'unique(external_order_id)',
            'The external order already exists.'
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'integration.order'
                )
        return super().create(vals_list)


    def add_log(self, level, message):
        self.ensure_one()

        return self.env['integration.log'].create({
            'integration_sale_order_id': self.id,
            'level': level,
            'message': message,
        })
    
    def _cron_proccess_order(self):
        oders_pending = self.search([('state', '=', 'pending')])

        for order in oders_pending:
            try:
                order._process_order()

            except Exception as error:
                order.write({
                    'state': 'failed',
                })

                order.add_log(
                    'error',
                    str(error),
                )
    
    def _process_order(self):
        self.ensure_one()
        partner_id = self._customer_process(self.payload.get('customer'))
        sale_id = self._create_sale_order(partner_id, self.payload)

        return sale_id


    def _customer_process(self, customer):
        Partner = self.env['res.partner']
        partner_id = Partner.search(
            domain=[
                ('vat', '=', customer.get('vat'))
            ],
            limit=1,
        )

        if partner_id:
            vals_to_update = {
                field: value
                for field, value in customer.items()
                if partner_id[field] != value
            }

            if vals_to_update:
                partner_id.write(vals_to_update)
                self.add_log('info', f'Customer updated. Fields: {list(vals_to_update.keys())}')
            
            return partner_id

        partner_id = Partner.create({
            field : value
            for field, value in customer.items()
        })
        self.add_log('info', f'Customer {customer.get("name")} created.')
        
        return partner_id
    
    def _create_sale_order(self, partner_id, payload):
        Sale = self.env['sale.order']

        order_lines = [
            (0, 0, {
                'product_id': line['product_id'],
                'product_uom_qty': line['quantity'],
                'price_unit': line['price'],
            })
            for line in payload.get('lines')
        ]

        sale_id = Sale.create({
            'partner_id': partner_id.id,
            'order_line': order_lines
        })
        self.add_log('info', f'Order {sale_id.name} successfully created.')

        self.write({
            'state': 'processed',
            'sale_id': sale_id.id,
            'processed_at': fields.Datetime.now(),
        })

        return sale_id

class IntegrationLog(models.Model):
    _name = 'integration.log'
    _description = 'Integration Log'
    
    integration_sale_order_id = fields.Many2one(
        comodel_name='integration.sale.order',
        required=True,
        ondelete='cascade',
    )

    level = fields.Selection(
        selection=[
            ('info', 'INFO'),
            ('warning', 'WARNING'),
            ('error', 'ERROR'),
        ],
        required=True,
        default='info',
    )

    message = fields.Text(
        required=True,
    )
