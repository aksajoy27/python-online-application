--DROP TABLE cart_items;
--DROP TABLE products;

--DROP TABLE order;

CREATE TABLE IF NOT EXISTS cart_items (
  user_id VARCHAR(20) NOT NULL,
  product_id VARCHAR(10) NOT NULL,
  quantity INTEGER NOT NULL,
  PRIMARY KEY (user_id, product_id)
);

CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(10) PRIMARY KEY,
  name VARCHAR(100),
  description TEXT,
  picture VARCHAR(100),
  price INTEGER
);


CREATE TABLE IF NOT EXISTS "order" (
  "order_id" varchar(100),
  "email" varchar(50),
  "amount" float,
  PRIMARY KEY ("order_id", "email")
);

CREATE TABLE IF NOT EXISTS "users" (
  "id" varchar(100),
  "email" varchar(50),
  "first_name" TEXT,
  "last_name" TEXT,
  PRIMARY KEY ("id", "email")
);
-- select * from cart_items WHERE product_id = 'L8ECAV7KIM';