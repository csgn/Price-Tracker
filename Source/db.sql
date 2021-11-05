CREATE DATABASE Tracker;

CREATE TABLE Subcategory (
    SubcategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    PRIMARY KEY (SubcategoryID)
);

CREATE TABLE Category (
    CategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    SubcategoryID int not null,
    PRIMARY KEY (CategoryID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);

CREATE TABLE Rate (
    RateID serial,
    Score float,
    Date timestamp not null,
    PRIMARY KEY (RateID)
);

CREATE TABLE Brand (
    BrandID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    RateID int not null,
    PRIMARY KEY (BrandID),
    FOREIGN KEY (RateID)
        REFERENCES Rate (RateID)
);

CREATE TABLE Supplier (
    SupplierID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    RateID int not null,
    PRIMARY KEY (SupplierID),
    FOREIGN KEY (RateID)
        REFERENCES Rate (RateID)
);

CREATE TABLE Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null,
    PRIMARY KEY (PriceID)
);

CREATE TABLE Product (
    ProductID serial,
    Name varchar(255) not null,
    Images varchar(255) array,
    URL varchar(255) not null,
    RateID int not null,
    PriceID int not null,
    BrandID int not null,
    CategoryID int not null,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (RateID)
        REFERENCES Rate (RateID),
    FOREIGN KEY (PriceID)
        REFERENCES Price (PriceID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID)
);

CREATE TABLE CategoryOwnedBySupplier (
    SupplierID int,
    CategoryID int,
    PRIMARY KEY (SupplierID, CategoryID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier(SupplierID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID)
);

CREATE TABLE CategoryOwnedByBrand (
    BrandID int,
    CategoryID int,
    PRIMARY KEY (CategoryID, BrandID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID)
);

CREATE TABLE ProductOwnedBySupplier (
    ProductID int,
    SupplierID int,
    PRIMARY KEY (ProductID, SupplierID),
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID)
);

CREATE TABLE SubcategoryOwnedBySupplier (
    SupplierID int,
    SubcategoryID int,
    PRIMARY KEY (SupplierID, SubcategoryID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);

CREATE TABLE ProductOwnedBySubcategory (
    ProductID int,
    SubcategoryID int,
    PRIMARY KEY (ProductID, SubcategoryID),
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);

CREATE TABLE SubcategoryOwnedByBrand (
    SubcategoryID int,
    BrandID int,
    PRIMARY KEY (SubcategoryID, BrandID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID)
);
