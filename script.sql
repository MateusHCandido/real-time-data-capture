--step 1: Create table sales
CREATE TABLE sales(
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    amount DECIMAL(10,2),
    sales_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Create notify_sales_changes function
CREATE OR REPLACE FUNCTION notify_sales_changes() 
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o evento é um INSERT para evitar possíveis erros
    IF TG_OP = 'INSERT' THEN
        PERFORM pg_notify('sales_channel', row_to_json(NEW)::text);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Create sales_trigger trigger
CREATE TRIGGER sales_trigger
AFTER INSERT ON sales
FOR EACH ROW
EXECUTE FUNCTION notify_sales_changes();


INSERT INTO sales (customer_name, amount) VALUES ('Alice', 150.00);
INSERT INTO sales (customer_name, amount) VALUES ('Bob', 250.00);



