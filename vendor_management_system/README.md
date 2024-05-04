
# Vendor Management System with Performance Metrics

This project is a Vendor Management System developed using Django and Django REST Framework. The system allows to manage vendor profiles, track purchase orders, and calculate vendor performance metrics such as on-time delivery rate, quality rating average, response time, and fulfillment rate.




## Features

- Vendor Profile Management: Create, retrieve, update, and delete vendor profiles. Each vendor profile includes essential information such as name, contact details, address, and a unique vendor code.
- Purchase Order Tracking: Track purchase orders with details including PO number, vendor reference, order date, items, quantity, and status.

- Vendor Performance Evaluation: Calculate and display performance metrics for vendors, including on-time delivery rate, quality rating average, response time, and fulfillment rate.


## Installation
1.Clone the repository:
```bash
https://github.com/s1999-alt/Vendor-Management.git
```

2.Create and activate Environment:
```bash
python3 -m venv env

windows : .env\Scripts\activate
Linux   :  source env/bin/activate
```

3.Path to Project File

```bash
 cd .\vendor_management_system\        
```

4.Install dependencies:

```bash
pip install -r requirements.txt
```

5.Apply database migrations:

```bash
python manage.py migrate
```

6.Run the development server:

```bash
python manage.py runserver

```






## Authentication
To access the API endpoints, authentication is required.

1.Create a superuser:

```bash
python manage.py createsuperuser
```



## API Reference

### Login

```http
  POST /api/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. SuperUser's username|
| `password` | `string` | **Required**. SuperUser's password|

After Login , We got an access token and refresh token, access token is required for all other endpoints


### Vendor Endpoints

#### 1. Create a new vendor.

```http
  POST /api/vendors/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Vendor name |
| `contact_details ` | `string` | **Required**. Vendor's contact details |
| `address` | `string` | **Required**. address |
| `vendor_code` | `string` | **Required**. vendor_code |



#### 2. List all vendors

```http
  GET /api/vendors/
```


#### 3. Retrieve a specific vendor's details.

```http
  GET /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor whose details are to be retrieved.|


#### 4. Update a vendor's details. 

```http
  PUT /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor.|
| `name` | `string` | **Required**. Vendor name |
| `contact_details ` | `string` | **Required**. Vendor's contact details |
| `address` | `string` | **Required**. address |
| `vendor_code` | `string` | **Required**. vendor_code |


#### 5. Delete a vendor.

```http
  DELETE /api/vendors/<vendor_id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_id`      | `integer` | **Required**. ID of the vendor.|




### Purchase Order Endpoints

#### 1. Create a purchase order.

```http
  POST /api/purchase_orders/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_number` | `string` | **Required**. Purchase order number(It Generates Automatically) |
| `vendor` | `integer` | **Required**. Vendor ID |
| `order_date` | `string` | **Required**. Order date (YYYY-MM-DD) |
| `delivery_date` | `string` | **Required**. delivery_date (YYYY-MM-DD) |
| `items` | `json` | **Required**.  Items in the purchase order |
| `quantity` | `integer` | **Required**. Total quantity of items|
| `status` | `string` | **Required**. Status of the purchase order |
| `quality_rating` | `integer` | **Required**. Rating given to the vendor |
| `issue_date` | `string` | **Required**. issue_date (YYYY-MM-DD) (Current date comes automatically) |
| `acknowledgment_date` | `string` | **Required**. acknowledgment_date (YYYY-MM-DD) |


#### 2. List all Purchase Orders

```http
  GET /api/purchase_orders/
```


#### 3. Retrieve details of a specific purchase order.

```http
  GET /api/purchase_orders/<po_id>/:
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |



#### 4. Update a purchase order.

```http
  PUT /api/purchase_orders/<po_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |
| `po_number` | `string` | **Required**. Purchase order number(It Generates Automatically) |
| `vendor` | `integer` | **Required**. Vendor ID |
| `order_date` | `string` | **Required**. Order date (YYYY-MM-DD) |
| `delivery_date` | `string` | **Required**. delivery_date (YYYY-MM-DD) |
| `items` | `json` | **Required**.  Items in the purchase order |
| `quantity` | `integer` | **Required**. Total quantity of items|
| `status` | `string` | **Required**. Status of the purchase order |
| `quality_rating` | `integer` | **Required**. Rating given to the vendor |
| `issue_date` | `string` | **Required**. issue_date (YYYY-MM-DD) (Current date comes automatically) |
| `acknowledgment_date` | `string` | **Required**. acknowledgment_date (YYYY-MM-DD) |


#### 5. Delete a Purchase Order

```http
  DELETE /api/purchase_orders/<po_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID |



### Retrieve Vendor Performance Metrics Endpoint

```http
  GET /api/vendors/<vendor_id>/performance/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_id` | `integer` | **Required**. Vendor ID|


### Update Acknowledgment Endpoint:

```http
  PUT purchase_orders/<po_id>/acknowledge/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_id` | `integer` | **Required**. Purchase Order ID|




## Running Tests

Run unit tests to validate the functionality of API endpoints:

```bash
  python manage.py test vendors
```

