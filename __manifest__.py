{
    "name": "Milima Sale Guard (Kenya eTIMS PIN Validation)",
    "version": "1.0.0",
    "category": "Sales/Sales",
    "summary": "Enforces mandatory KRA PIN for Kenyan customers before confirming Sales Orders.",
    "description": """
Milima Sale Guard
=================
This add-on closes an essential compliance gap for Kenyan hardware and building suppliers:
preventing sales staff from confirming sales orders to Kenyan customers who lack a registered KRA PIN.

Because KRA eTIMS strictly requires a valid customer PIN on B2B / trade credit invoices, confirming orders
without a PIN leads to failed invoice transmissions or manual correction work at the counter.

Key Features:
- Blocks sales order confirmation if commercial partner is Kenyan and has no Tax ID (KRA PIN).
- Displays clear, actionable error message instructing staff on what to fix.
- Ignores non-Kenyan export customers.
- Fully compatible with standard Odoo upgrades (clean model override, no core edits).
    """,
    "author": "Elias Maina",
    "website": "https://github.com/Elias-3817/milima_sale_guard",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "l10n_ke",
    ],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
