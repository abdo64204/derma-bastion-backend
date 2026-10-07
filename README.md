# Derma Bastion - Django Backend

A production-ready Django REST Framework backend designed to power the [Derma Bastion Frontend](file:///Users/abdomo/Desktop/derma/derma-bastion-frontend) e-commerce store.

---

## 🎯 Architecture & Features Overview

The backend was specifically engineered around the frontend models, services, and workflows:

| Django App | Purpose & Frontend Alignment | Key Endpoints |
| :--- | :--- | :--- |
| **`products`** | Complete bilingual product catalog (English + Arabic), category filtering (Skin Care, Hair Care, Eye Care), live search, price sorting, and best sellers. | `GET /api/products/`<br>`GET /api/products/?category=`<br>`GET /api/products/?search=`<br>`GET /api/products/?sort=`<br>`GET /api/products/best-sellers/`<br>`GET /api/products/<id>/` |
| **`orders`** | Full checkout processing matching frontend `Order` & `DeliveryDetails`, Egyptian phone validation (`01[0125]XXXXXXXX`), multiple payment methods (`cod`, `card`, `vodafone_cash`, `instapay`), and live 5-step tracking timeline. | `POST /api/orders/`<br>`GET /api/orders/<id>/`<br>`GET /api/orders/track/?order=DB-XXXXXX`<br>`POST /api/orders/<id>/receipt/` |
| **`store_settings`** | Dynamic store owner configuration matching `STORE_PAYMENT_CONFIG` (Vodafone Cash wallet number, InstaPay IPA, Card gateway mode), shipping thresholds (Free shipping >= 1500 EGP, otherwise 60 EGP), and contact info. | `GET /api/store-config/` |
| **`contact`** | Customer inquiries and contact message submissions directly from the Contact page. | `POST /api/contact/` |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (Python 3.9.6 supported)

### 2. Activate Virtual Environment
```bash
cd /Users/abdomo/Desktop/derma/derma-bastion-backend
source .venv/bin/activate
```

### 3. Run Migrations & Seed Data
```bash
# 1. Apply database migrations
python manage.py migrate

# 2. Seed initial 8 products with full English & Arabic details
python manage.py seed_products

# 3. Create default admin superuser (admin / admin123456)
python manage.py init_admin
```

### 4. Run Development Server
```bash
python manage.py runserver 8000
```
The API is now running at `http://localhost:8000/api/` and the Admin Portal at `http://localhost:8000/admin/`.

---

## 🛡️ Django Admin Portal (`/admin/`)

The admin interface has been heavily customized for store management and manual payment verification:

- **Order Management & Fulfillment**:
  - Filter by fulfillment status (`Placed`, `Confirmed`, `Shipped`, `Out for Delivery`, `Delivered`).
  - Filter by payment method (`Cash on Delivery`, `Vodafone Cash`, `InstaPay`, `Credit Card`).
  - Search by Order ID (`DB-XXXXXX`), customer name, Egyptian phone, city, or address.
  - Action buttons:
    - *Verify payment for selected orders*
    - *Advance fulfillment to Confirmed / Shipped / Out for Delivery / Delivered*
- **Payment Verification Workflow (Vodafone Cash & InstaPay)**:
  - Customers upload transfer confirmation screenshots during checkout.
  - Admin displays an inline receipt thumbnail and a click-to-enlarge preview in full resolution.
  - Store managers inspect the transfer and click **Verify Payment** to confirm the order.
- **Product Catalog Management**:
  - Full CRUD for products, prices, stock, badges, benefits, ingredients, and Arabic translations.
- **Store Configuration**:
  - Modify Vodafone Cash merchant number, InstaPay Payment Address (IPA), free shipping thresholds, and header announcements without redeploying code.

---

## 📡 API Reference

### 1. Products API

#### `GET /api/products/`
Returns the active product catalog. Serializer matches the frontend `Product` interface.

**Query Parameters:**
- `category`: Filter by category (`skin`, `hair`, `eye`, or `all`).
- `search`: Case-insensitive search on name, Arabic name, category, ingredients, and description.
- `sort`: `priceAsc` (low to high), `priceDesc` (high to low), or `featured`.

**Sample Response:**
```json
[
  {
    "id": 1,
    "name": "Hyaluronic Acid Serum 30ml",
    "category": "Skin Care",
    "price": 550.0,
    "image": "",
    "badge": "Best Seller",
    "description": "A lightweight serum that gives skin a fresh, hydrated look and feel.",
    "benefits": [
      "Lightweight, non-greasy texture",
      "Absorbs quickly",
      "Suitable for daily use"
    ],
    "howToUse": "Apply 2-3 drops to clean skin morning and evening, then follow with moisturizer.",
    "ingredients": "Water, Hyaluronic Acid, Glycerin, Panthenol.",
    "ar": {
      "name": "سيروم حمض الهيالورونيك 30 مل",
      "category": "العناية بالبشرة",
      "badge": "الأكثر مبيعاً",
      "description": "سيروم خفيف يمنح البشرة مظهراً وملمساً منتعشاً ومرطباً.",
      "benefits": ["قوام خفيف غير دهني", "سريع الامتصاص", "مناسب للاستخدام اليومي"],
      "howToUse": "ضع 2-3 قطرات على بشرة نظيفة صباحاً ومساءً، ثم استخدم المرطب.",
      "ingredients": "ماء، حمض الهيالورونيك، جلسرين، بانثينول."
    }
  }
]
```

#### `GET /api/products/best-sellers/`
Returns best selling products (marked with `is_best_seller` or "Best Seller" badge).

#### `GET /api/products/<id>/`
Returns detailed information for a single product.

---

### 2. Orders API

#### `POST /api/orders/`
Place a new order. Accepts JSON or Multipart form data.

**Request Payload:**
```json
{
  "delivery": {
    "fullName": "Ahmed Mohamed",
    "phone": "01012345678",
    "governorate": "Cairo",
    "city": "Nasr City",
    "address": "15 Abbas El Akkad Street, Building 4",
    "notes": "Please call before arrival"
  },
  "items": [
    {
      "product": {
        "id": 1,
        "name": "Hyaluronic Acid Serum 30ml",
        "category": "Skin Care",
        "price": 550.0
      },
      "quantity": 2
    }
  ],
  "subtotal": 1100.0,
  "shipping": 60.0,
  "total": 1160.0,
  "payment": {
    "method": "vodafone_cash",
    "status": "pending",
    "receipt": {
      "fileName": "vodafone_receipt.png",
      "fileSize": 142050,
      "fileType": "image/png",
      "dataUrl": "data:image/png;base64,iVBORw0KGgoAAA..."
    }
  }
}
```

**Response (`201 Created`):**
```json
{
  "id": "DB-482913",
  "createdAt": "2026-10-07T14:50:00Z",
  "delivery": {
    "fullName": "Ahmed Mohamed",
    "phone": "01012345678",
    "governorate": "Cairo",
    "city": "Nasr City",
    "address": "15 Abbas El Akkad Street, Building 4",
    "notes": "Please call before arrival"
  },
  "items": [ ... ],
  "subtotal": 1100.0,
  "shipping": 60.0,
  "total": 1160.0,
  "payment": {
    "method": "vodafone_cash",
    "status": "pending",
    "receipt": {
      "fileName": "receipt_DB-482913.png",
      "dataUrl": "http://localhost:8000/media/receipts/2026/10/receipt_DB-482913.png"
    }
  },
  "status": "placed",
  "timeline": {
    "currentStepIndex": 0,
    "status": "placed",
    "placedAt": "2026-10-07T14:50:00Z"
  }
}
```

#### `GET /api/orders/<id>/` or `GET /api/orders/track/?order=DB-XXXXXX`
Fetches the order by its ID for the order confirmation page (`/order-success/:id`) and tracking page (`/track`).

---

### 3. Store Config API

#### `GET /api/store-config/`
Returns store configurations so the frontend does not have to hardcode wallet numbers or delivery policies:
```json
{
  "currency": "EGP",
  "vodafoneCash": {
    "walletNumber": "01000000000",
    "merchantName": "Derma Bastion Official",
    "isConfigured": true
  },
  "instapay": {
    "identifier": "dermabastion@instapay",
    "accountName": "Derma Bastion Official",
    "isConfigured": true
  },
  "cardGateway": {
    "providerName": "Paymob",
    "isLiveGatewayConnected": false
  },
  "shipping": {
    "freeShippingFrom": 1500.0,
    "shippingFee": 60.0,
    "currency": "EGP"
  },
  "contact": {
    "phone": "+20 100 000 0000",
    "whatsappNumber": "201000000000",
    "email": "hello@dermabastion.com"
  }
}
```

---

### 4. Contact Inquiries API

#### `POST /api/contact/`
Submits inquiries sent from the contact form:
```json
{
  "name": "Sarah Hassan",
  "email": "sarah@example.com",
  "phone": "01234567890",
  "subject": "Order DB-482913 inquiry",
  "message": "When will my order arrive?"
}
```

---

## 🔌 Connecting Angular Frontend to this Backend

To connect the Angular app (`derma-bastion-frontend`) to this backend:

1. In Angular `src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api'
   };
   ```

2. Replace static arrays in `src/app/services/product-data.ts`:
   ```typescript
   import { HttpClient } from '@angular/common/http';
   // fetch products via http.get<Product[]>(`${environment.apiUrl}/products/`)
   ```

3. Update `src/app/services/orders.ts`:
   ```typescript
   // create order via http.post<Order>(`${environment.apiUrl}/orders/`, payload)
   // track order via http.get<Order>(`${environment.apiUrl}/orders/track/?order=${orderNumber}`)
   ```
