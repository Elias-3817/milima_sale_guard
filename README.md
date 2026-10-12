# Milima Sale Guard (`milima_sale_guard`)

**Odoo Module: Enforcing Mandatory KRA PIN for Kenyan Sales Orders**

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-green.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)

> **Notice:** Developed as part of a functional demonstration case study for *Milima Hardware & Building Supplies Ltd*. All company names and test data are fictional for evaluation purposes.

---

## 1. Business Context & Problem

In Kenya, the **Kenya Revenue Authority (KRA)** requires electronic tax invoices generated via **eTIMS** (electronic Tax Invoice Management System). 

For Kenyan hardware distributors and building supply merchants like **Milima Hardware & Building Supplies Ltd**:
- Contractors and commercial buyers frequently order cement, steel, and timber on credit.
- Counter sales staff often confirm Sales Orders without capturing the customer's KRA PIN.
- When the invoice is posted later, KRA eTIMS rejects the electronic transmission, forcing accounting staff to hunt down the PIN or issue manual credit notes.

Standard Odoo settings warn on credit limits, but **standard Odoo does not block order confirmation if a domestic customer has no Tax ID / PIN**.

---

## 2. Solution

`milima_sale_guard` is a lightweight Odoo module that hooks into the sales order confirmation action:
1. When a salesperson clicks **Confirm**:
   - The module checks the customer's commercial entity.
   - If the customer is located in **Kenya (`country_id.code == 'KE'`)** and has **no Tax ID / KRA PIN**, confirmation is blocked with a clear message:
     > *"This customer has no KRA PIN. eTIMS invoices need one. Add it on the customer before confirming."*
2. **Export / Non-Kenyan customers** (e.g. clients from Uganda, Tanzania) are automatically bypassed.
3. Once the salesperson adds the PIN on the customer card, the order confirms immediately.

---

## 3. Architecture & Upgrade Safety

- **Zero Core Edits:** Does not touch any of Odoo's core Python or XML code.
- **Model Inheritance:** Inherits `sale.order` and overrides `action_confirm()` using `super()`.
- **Upgrade Friendly:** Safe across minor and major Odoo version upgrades.

```
sale.order.action_confirm()
  │
  ├──► Check partner country == 'KE'?
  │      ├── No  ──► Call super().action_confirm() (Allow)
  │      └── Yes ──► Check partner Tax ID / PIN exists?
  │                    ├── Yes ──► Call super().action_confirm() (Allow)
  │                    └── No  ──► Raise UserError (Block)
```

---

## 4. Automated Tests

The module includes unit tests covering all operational cases:
1. `test_blocks_kenyan_customer_without_pin`: Ensures Kenyan customers without PIN cannot confirm orders.
2. `test_allows_kenyan_customer_with_pin`: Verifies orders confirm normally once a valid PIN is present.
3. `test_ignores_foreign_customer_without_pin`: Ensures export orders remain unaffected.

### Running the Tests:
```bash
python3 odoo-bin -c odoo.conf -d milima_test -i milima_sale_guard --test-enable --stop-after-init
```

---

## 5. Run It Locally with Docker

1. Put this `docker-compose.yml` in the folder that **contains** `milima_sale_guard/`:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: postgres
    volumes:
      - db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:19
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./milima_sale_guard:/mnt/extra-addons/milima_sale_guard:ro
      - odoo-data:/var/lib/odoo

volumes:
  db-data:
  odoo-data:
```

2. Create a database with Sales, Kenya localization and the add-on installed:

```bash
docker compose up -d db
docker compose run --rm odoo odoo -d milima -i sale_management,l10n_ke,milima_sale_guard --stop-after-init
```

3. Start Odoo and open http://localhost:8069 (login `admin` / `admin`):

```bash
docker compose up -d
```

4. Run the tests:

```bash
docker compose run --rm odoo odoo -d milima -u milima_sale_guard --test-tags /milima_sale_guard --stop-after-init
```

5. Stop it with `docker compose down` (add `-v` to wipe the database).

---

## 6. Author
**Elias Maina** -- Nairobi, Kenya  
