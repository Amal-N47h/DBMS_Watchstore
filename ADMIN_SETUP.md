# Django Admin Setup Guide

## Setup Instructions

### 1. Create a Superuser Account

To access the Django admin panel, you need to create a superuser account:

```bash
cd watchstore
python manage.py createsuperuser
```

Follow the prompts to enter:
- Username
- Email (optional)
- Password (twice for confirmation)

### 2. Run Migrations

Make sure all database migrations are applied:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start the Development Server

```bash
python manage.py runserver
```

### 4. Access the Admin Panel

Open your browser and go to:
```
http://localhost:8000/admin/
```

Login with the superuser credentials you created.

## Admin Features

### Products Management
- View all products with thumbnails
- Add/edit products with images
- Monitor stock levels with color-coded status:
  - 🔴 Red: Out of Stock (0 items)
  - 🟠 Orange: Low Stock (< 10 items)
  - 🟢 Green: In Stock (≥ 10 items)
- Search products by title, description, or brand
- Filter by brand or stock level

### Orders Management
- View all customer orders
- See order details including:
  - Customer information
  - Shipping address
  - Payment status
  - Order items and totals
- Filter by payment status, payment method, or date
- Search by order ID, customer email, or contact number

### Shopping Cart Management
- Monitor all cart items
- View active and ordered carts
- Filter by order status
- See subtotals for each cart item

### Users Management
- View all registered users
- Edit user information
- Set superuser permissions
- Search by username, email, or phone number

### Brands Management
- Add/edit watch brands
- See product count per brand

## Admin Customizations

The admin interface includes:
- ✅ Image thumbnails for products
- ✅ Stock status indicators
- ✅ Order totals and item summaries
- ✅ Search functionality on all models
- ✅ Advanced filtering options
- ✅ Date hierarchy for orders and carts
- ✅ Readonly calculated fields (totals, subtotals)
- ✅ Organized fieldsets for better UX

## Tips

1. **Image Upload**: When adding products, you can upload images which will be stored in the `media/products/` directory.

2. **Stock Management**: Always update stock when adding new products. The system automatically reduces stock when orders are placed.

3. **Order Tracking**: Use the date hierarchy filter to quickly find orders by date.

4. **Bulk Actions**: You can select multiple items and perform bulk actions (delete, etc.) using checkboxes.

## Troubleshooting

If you can't access the admin:
1. Make sure you created a superuser: `python manage.py createsuperuser`
2. Check that migrations are applied: `python manage.py migrate`
3. Verify the server is running on port 8000
4. Check browser console for any errors

