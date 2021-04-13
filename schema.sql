CREATE TABLE token (
    bearer varchar(64) PRIMARY KEY, 
    expiration_date DATE
);

CREATE TABLE profile(
    profile_id int AUTO_INCREMENT PRIMARY KEY, 
    email varchar(100) UNIQUE NOT NULL, 
    password varchar(50) NOT NULL, 
    phone_number varchar(10), 
    first_name varchar(50) NOT NULL, 
    last_name varchar(50) NOT NULL, 
    token_id VARCHAR(64), 
    CONSTRAINT FOREIGN KEY (token_id) REFERENCES token(bearer) ON DELETE CASCADE
);

CREATE TABLE client (
    profile_id int AUTO_INCREMENT PRIMARY KEY,
    payment_id varchar(150) UNIQUE, 
    contact_method varchar(50),
    CONSTRAINT FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
) ;

CREATE TABLE parlor (
	parlor_id int AUTO_INCREMENT PRIMARY KEY, 
    name varchar(50) not null, 
    address_line_1 varchar(200) NOT NULL, 
    address_line_2 varchar(200), 
    city varchar(100) NOT NULL, 
    state varchar(20) NOT NULL,
    zip varchar(10) NOT NULL, 
    shop_commission double NOT NULL
);

CREATE TABLE artist (
    profile_id int AUTO_INCREMENT PRIMARY KEY, 
    max_bookings int not null, 
    is_manager boolean not null,
    minimum_price int,
    parlor_id int, 
    CONSTRAINT FOREIGN KEY (profile_id) REFERENCES profile(profile_id),
    CONSTRAINT FOREIGN KEY (parlor_id) REFERENCES parlor(parlor_id)
);

CREATE TABLE booking (
    artist_id int, 
    client_id int, 
    booking_id int AUTO_INCREMENT PRIMARY KEY, 
    design_description varchar(500) not null, 
    design_approved boolean not null, 
    price int not null, 
    price_approved boolean not null, 
    FOREIGN KEY (artist_id) REFERENCES artist(profile_id),
   FOREIGN KEY (client_id) REFERENCES client(profile_id)
);

CREATE TABLE timeslot (
 	date_time DATETIME,
    booking_id int, 
    CONSTRAINT FOREIGN KEY (booking_id) REFERENCES booking(booking_id), 
    CONSTRAINT PRIMARY KEY (date_time, booking_id)
);


-- Functions and Procedures
---------------------------------

DROP PROCEDURE create_user; 
DELIMITER //

CREATE PROCEDURE create_user(IN bearer_token varchar(64), IN email varchar(64), IN my_password varchar(100), IN first_name varchar(50), IN last_name varchar(50))
BEGIN 
    INSERT INTO token (bearer, expiration_date) VALUES (bearer_token, CURDATE());
    INSERT INTO profile (email, first_name, last_name, password, token_id) VALUES (email, first_name, last_name, my_password, bearer_token);
END //

DELIMITER ;
