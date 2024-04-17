CREATE TABLE customer_infos(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone INT,
    rent_id INT
);

CREATE TABLE bike_info(
    bike_id INT PRIMARY KEY AUTO_INCREMENT,
    bike_name VARCHAR(255),
    bike_type VARCHAR(255),
    availability BOOLEAN DEFAULT TRUE
);

ALTER TABLE customer_infos
ADD CONSTRAINT fk_bike_rent
FOREIGN KEY (rent_id)
REFERENCES bike_info (bike_id);
