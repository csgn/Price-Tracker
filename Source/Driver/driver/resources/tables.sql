CREATE TABLE IF NOT EXISTS Category (
    CategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    PRIMARY KEY (CategoryID)
);

CREATE TABLE IF NOT EXISTS Subcategory (
    SubcategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null UNIQUE,
    CategoryID int not null,
    PRIMARY KEY (SubcategoryID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID)
);

CREATE TABLE IF NOT EXISTS Brand (
    BrandID serial,
    Name varchar(255) not null,
    URL varchar(255) not null UNIQUE,
    PRIMARY KEY (BrandID)
);

CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID serial,
    Name varchar(255) not null,
    Rate float,
    URL varchar(255) not null UNIQUE,
    PRIMARY KEY (SupplierID)
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID serial,
    Name varchar(255) not null,
    Images varchar(255) array,
    Rate float,
    URL varchar(255) not null UNIQUE,
    BrandID int not null,
    CategoryID int not null,
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID),
    PRIMARY KEY (ProductID)
);

CREATE TABLE IF NOT EXISTS Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null default now(),
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (PriceID)
);

CREATE TABLE IF NOT EXISTS CategoryOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    categoryid int REFERENCES category ON DELETE CASCADE,
    PRIMARY KEY (supplierid, categoryid)
);

CREATE TABLE IF NOT EXISTS CategoryOwnedByBrand (
    brandid int REFERENCES brand ON DELETE CASCADE,
    categoryid int REFERENCES category ON DELETE CASCADE,
    PRIMARY KEY (brandid, categoryid)
);

CREATE TABLE IF NOT EXISTS ProductOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (supplierid, productid)
);

CREATE TABLE IF NOT EXISTS SubcategoryOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    PRIMARY KEY (supplierid, subcategoryid)
);

CREATE TABLE IF NOT EXISTS ProductOwnedBySubcategory (
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (subcategoryid, productid)
);

CREATE TABLE IF NOT EXISTS SubcategoryOwnedByBrand (
    brandid int REFERENCES brand ON DELETE CASCADE,
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    PRIMARY KEY (brandid, subcategoryid)
);

CREATE TABLE IF NOT EXISTS BrandOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    brandid int REFERENCES brand ON DELETE CASCADE,
    PRIMARY KEY (supplierid, brandid)
);