# Vendor Management System API Documentation

This document provides detailed documentation for the Vendor Management System API.

## Authentication

Token-based authentication is required to access all API endpoints. Clients must include an authentication token in the `Authorization` header of each request.


## API Endpoints

### 1 . Login

#### POST /api/login/

Login for superuser.

After login with superuser's username and password, You got access token and refresh token.use that access token as bearer token for authorization.


### 2. Vendor Profile Management

#### 1. GET /api/vendors/

List all vendors.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: List of vendor objects.

#### 2 . POST /api/vendors/

Create a new vendor.

**Authentication:** Required

**Request body parameters:**
- `name` (string): Vendor's name.
- `contact_details` (string): Vendor's contact details (10 digits).
- `address` (string): Vendor's address.
- `vendor_code` (string): Unique vendor code.

**Response:**
- Status code: 201 Created
- Response body: Vendor object.

#### 3.  GET /api/vendors/<vendor_id>/

Retrieve a specific vendor's details.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: Vendor object.

#### 4. PUT /api/vendors/<vendor_id>/

Update a vendor's details.

**Authentication:** Required

**Request body parameters:**
- Same as POST /api/vendors/

**Response:**
- Status code: 200 OK
- Response body: Updated vendor object.

#### 5. DELETE /api/vendors/<vendor_id>/

Delete a vendor.

**Authentication:** Required

**Response:**
- Status code: 204 No Content


### 3. Purchase Order Tracking

#### 1. GET /api/purchase_orders/

List all purchase orders.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: List of purchase order objects.

#### 2. POST /api/purchase_orders/

Create a new purchase order.

**Authentication:** Required

**Request body parameters:**
- `po_number` (string): Unique PO number.
- `vendor` (integer): Vendor ID.
- `order_date` (string): Order date.
- `delivery_date` (string): Delivery date.
- `items` (object): Details of items ordered.
- `quantity` (integer): Total quantity of items.
- `status` (string): Current status of the PO.
- `quality_rating` (float, optional): Rating given to the vendor for this PO.

**Response:**
- Status code: 201 Created
- Response body: Purchase order object.

#### 3. GET /api/purchase_orders/<po_id>/

Retrieve details of a specific purchase order.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: Purchase order object.

#### 4. GET /api/purchase_orders/by_vendor/<vendor_id>/

Retrieve purchase orders by vendor.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: Purchase order object.

#### 5. PUT /api/purchase_orders/<po_id>/

Update a purchase order.

**Authentication:** Required

**Request body parameters:**
- Same as POST /api/purchase_orders/

**Response:**
- Status code: 200 OK
- Response body: Updated purchase order object.

#### 6. DELETE /api/purchase_orders/<po_id>/

Delete a purchase order.

**Authentication:** Required

**Response:**
- Status code: 204 No Content


### 4. Vendor Performance Evaluation

#### 1. GET /api/vendors/<vendor_id>/performance/

Retrieve a vendor's performance metrics.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: Vendor performance metrics.

### 5. Update Acknowledgment

#### 1. PUT api/purchase_orders/<po_id>/acknowledge/

update acknowledgment_date and trigger the recalculation of average_response_time.

**Authentication:** Required

**Response:**
- Status code: 200 OK
- Response body: Vendor object.

## Conclusion

This concludes the documentation for the Vendor Management System API. For any further details, contact the me or mail me.

## Contact Details

Phone : 9633911996

Email: siyadsavad313@gmail.com
