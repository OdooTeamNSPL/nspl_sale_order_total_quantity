from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_order_qty = fields.Float(string="Total Ordered Qty", compute='_compute_sale_quantities', store=True)
    total_delivered_qty = fields.Float(string="Total Delivered Qty", compute='_compute_sale_quantities', store=True)
    total_invoiced_qty = fields.Float(string="Total Invoiced Qty", compute='_compute_sale_quantities', store=True)
    pending_delivery_qty = fields.Float(string="Pending Delivery Qty", compute='_compute_sale_quantities')
    pending_invoice_qty = fields.Float(string="Pending Invoice Qty", compute='_compute_sale_quantities')

    @api.depends('order_line.product_uom_qty', 'order_line.qty_delivered', 'order_line.qty_invoiced', 'order_line.product_id.type')
    def _compute_sale_quantities(self):
        for order in self:
            total_order = total_delivered = total_invoiced = 0.0
            for line in order.order_line:

                if line.product_id.type != 'service':
                    total_order += line.product_uom_qty
                    total_delivered += line.qty_delivered
                total_invoiced += line.qty_invoiced

            order.total_order_qty = total_order
            order.total_delivered_qty = total_delivered
            order.total_invoiced_qty = total_invoiced
            order.pending_delivery_qty = total_order - total_delivered
            order.pending_invoice_qty = total_order - total_invoiced
