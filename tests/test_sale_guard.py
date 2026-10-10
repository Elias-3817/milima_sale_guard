# Part of Milima Hardware Odoo Implementation.
from odoo.tests import tagged, TransactionCase
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class TestSaleGuard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_ke = cls.env.ref("base.ke")
        cls.country_ug = cls.env.ref("base.ug")

        # Test product
        cls.product = cls.env["product.product"].create({
            "name": "Bamburi Tembo Cement 50kg",
            "type": "consu",
            "list_price": 780.0,
        })

        # Customer 1: Kenyan with NO PIN
        cls.customer_no_pin = cls.env["res.partner"].create({
            "name": "Jua Kali Contractor (No PIN)",
            "country_id": cls.country_ke.id,
            "vat": False,
        })

        # Customer 2: Kenyan with VALID PIN
        cls.customer_with_pin = cls.env["res.partner"].create({
            "name": "Apex Ridge Builders Ltd",
            "country_id": cls.country_ke.id,
            "vat": "P051293847X",
        })

        # Customer 3: Foreign customer (Uganda) without KRA PIN
        cls.customer_foreign = cls.env["res.partner"].create({
            "name": "Kampala Hardware Importers",
            "country_id": cls.country_ug.id,
            "vat": False,
        })

    def test_blocks_kenyan_customer_without_pin(self):
        """Confirming an order for a Kenyan customer with no KRA PIN must raise UserError."""
        order = self.env["sale.order"].create({
            "partner_id": self.customer_no_pin.id,
            "order_line": [
                (0, 0, {
                    "product_id": self.product.id,
                    "product_uom_qty": 50.0,
                    "price_unit": 780.0,
                })
            ]
        })
        with self.assertRaises(UserError) as cm:
            order.action_confirm()
        self.assertIn("This customer has no KRA PIN", str(cm.exception))

    def test_allows_kenyan_customer_with_pin(self):
        """Confirming an order for a Kenyan customer with a valid KRA PIN must succeed."""
        order = self.env["sale.order"].create({
            "partner_id": self.customer_with_pin.id,
            "order_line": [
                (0, 0, {
                    "product_id": self.product.id,
                    "product_uom_qty": 50.0,
                    "price_unit": 780.0,
                })
            ]
        })
        order.action_confirm()
        self.assertEqual(order.state, "sale")

    def test_ignores_foreign_customer_without_pin(self):
        """Confirming an export order for a non-Kenyan customer without KRA PIN must pass without error."""
        order = self.env["sale.order"].create({
            "partner_id": self.customer_foreign.id,
            "order_line": [
                (0, 0, {
                    "product_id": self.product.id,
                    "product_uom_qty": 10.0,
                    "price_unit": 780.0,
                })
            ]
        })
        order.action_confirm()
        self.assertEqual(order.state, "sale")
