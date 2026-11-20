
CREATE TABLE IF NOT EXISTS retail.customers (
    customer_id BIGINT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(100),
    city VARCHAR(150),
    province VARCHAR(150),
    country VARCHAR(100),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS retail.stores (
    store_id BIGINT PRIMARY KEY,
    store_name VARCHAR(255),
    city VARCHAR(150),
    province VARCHAR(150),
    country VARCHAR(100),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS retail.products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(150),
    brand VARCHAR(150),
    price NUMERIC(12,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS retail.employees (
    employee_id BIGINT PRIMARY KEY,
    store_id BIGINT REFERENCES retail.stores(store_id),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    job_title VARCHAR(150),
    salary NUMERIC(12,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS retail.orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES retail.customers(customer_id),
    store_id BIGINT REFERENCES retail.stores(store_id),
    order_timestamp TIMESTAMP,
    payment_method VARCHAR(100),
    order_status VARCHAR(50),
    total_amount NUMERIC(14,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);

CREATE TABLE IF NOT EXISTS retail.order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT REFERENCES retail.orders(order_id),
    product_id BIGINT REFERENCES retail.products(product_id),
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    line_amount NUMERIC(14,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active VARCHAR(1)
);
