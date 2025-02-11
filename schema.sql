-- schema.sql
-- Drop tables if they exist
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS product_type;
DROP TABLE IF EXISTS employees;

-- Create product_type table
CREATE TABLE product_type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    type_id INTEGER REFERENCES product_type(type_id),
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    sku VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create prices table
CREATE TABLE prices (
    price_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    base_price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    effective_from DATE NOT NULL,
    effective_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE NOT NULL,
    termination_date DATE,
    role VARCHAR(50),
    department VARCHAR(50),
    manager_id INTEGER REFERENCES employees(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sales table
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    employee_id INTEGER REFERENCES employees(employee_id),
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for better performance
CREATE INDEX idx_products_type_id ON products(type_id);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_employee_id ON sales(employee_id);
CREATE INDEX idx_prices_product_id ON prices(product_id);
CREATE INDEX idx_sales_date ON sales(sale_date);

-- Insert sample data for product_type
INSERT INTO product_type (type_name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and publications'),
('Home & Garden', 'Home improvement and garden supplies');

-- Insert sample products
INSERT INTO products (type_id, product_name, sku, description) VALUES
(1, 'Smartphone X', 'SMX001', 'Latest smartphone model'),
(1, 'Laptop Pro', 'LPT001', 'Professional laptop'),
(2, 'Cotton T-Shirt', 'CTS001', 'Comfortable cotton t-shirt'),
(3, 'Python Programming', 'BOK001', 'Programming guide');

-- Insert sample employees
INSERT INTO employees (first_name, last_name, email, phone, hire_date, role, department) VALUES
('John', 'Doe', 'john.doe@example.com', '555-0101', '2023-01-15', 'Sales Rep', 'Sales'),
('Jane', 'Smith', 'jane.smith@example.com', '555-0102', '2023-02-01', 'Sales Manager', 'Sales'),
('Bob', 'Johnson', 'bob.johnson@example.com', '555-0103', '2023-03-01', 'Sales Rep', 'Sales');

-- Insert sample prices
INSERT INTO prices (product_id, base_price, effective_from) VALUES
(1, 999.99, '2023-01-01'),
(2, 1499.99, '2023-01-01'),
(3, 29.99, '2023-01-01'),
(4, 49.99, '2023-01-01');

-- Insert sample sales
INSERT INTO sales (product_id, employee_id, sale_date, quantity, unit_price, total_amount) VALUES
(1, 1, '2023-04-01', 1, 999.99, 999.99),
(2, 2, '2023-04-02', 1, 1499.99, 1499.99),
(3, 1, '2023-04-03', 2, 29.99, 59.98),
(4, 3, '2023-04-04', 1, 49.99, 49.99);