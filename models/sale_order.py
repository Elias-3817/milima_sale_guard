# Part of Milima Hardware Odoo Implementation.
from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Validate that any Kenyan commercial partner has a KRA PIN (vat)
        before allowing the sales order to be confirmed.
        """
        for order in self:
            partner = order.partner_id.commercial_partner_id
            is_kenyan = partner.country_id and partner.country_id.code == "KE"
            has_no_pin = not partner.vat or not partner.vat.strip()

            if is_kenyan and has_no_pin:
                raise UserError(_(
                    "This customer has no KRA PIN. eTIMS invoices need one. "
                    "Add it on the customer before confirming."
                ))

        return super().action_confirm()
