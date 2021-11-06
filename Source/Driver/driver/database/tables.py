__subcategory = """
CREATE TABLE IF NOT EXISTS Subcategory (
    SubcategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    PRIMARY KEY (SubcategoryID)
);
"""

__category = """
CREATE TABLE IF NOT EXISTS Category (
    CategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    SubcategoryID int not null,
    PRIMARY KEY (CategoryID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);
"""

__rate = """
CREATE TABLE IF NOT EXISTS Rate (
    RateID serial,
    Score float,
    Date timestamp not null,
    PRIMARY KEY (RateID)
);
"""

__brand = """
CREATE TABLE IF NOT EXISTS Brand (
    BrandID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    PRIMARY KEY (BrandID)
);
"""

__supplier = """
CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    RateID int not null,
    PRIMARY KEY (SupplierID),
    FOREIGN KEY (RateID)
        REFERENCES Rate (RateID)
);
"""

__price = """
CREATE TABLE IF NOT EXISTS Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null,
    PRIMARY KEY (PriceID)
);
"""

__product = """
CREATE TABLE IF NOT EXISTS Product (
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
"""

__categoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS CategoryOwnedBySupplier (
    SupplierID int,
    CategoryID int,
    PRIMARY KEY (SupplierID, CategoryID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier(SupplierID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID)
);
"""

__categoryownedbybrand = """
CREATE TABLE IF NOT EXISTS CategoryOwnedByBrand (
    CategoryID int REFERENCES Category,
    BrandID int REFERENCES Brand,
    PRIMARY KEY (CategoryID, BrandID)
);
"""

__productownedbysupplier = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySupplier (
    ProductID int,
    SupplierID int,
    PRIMARY KEY (ProductID, SupplierID),
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID)
);
"""

__subcategoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedBySupplier (
    SupplierID int,
    SubcategoryID int,
    PRIMARY KEY (SupplierID, SubcategoryID),
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);
"""

__productownedbysubcategory = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySubcategory (
    ProductID int,
    SubcategoryID int,
    PRIMARY KEY (ProductID, SubcategoryID),
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID)
);
"""

__subcategoryownedbybrand = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedByBrand (
    SubcategoryID int,
    BrandID int,
    PRIMARY KEY (SubcategoryID, BrandID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID)
);
"""

STATIC_TABLES = {
    "Subcategory": __subcategory,
    "Category": __category,
    "Rate": __rate,
    "Brand": __brand,
    "Supplier": __supplier,
    "Price": __price,
    "Product": __product,
    "CategoryOwnedBySupplier": __categoryownedbysupplier,
    "CategoryOwnedByBrand": __categoryownedbybrand,
    "ProductOwnedBySupplier": __productownedbysupplier,
    "ProductOwnedBySubcategory": __productownedbysubcategory,
    "SubcategoryOwnedByBrand": __subcategoryownedbybrand,
    "SubcategoryOwnedBySupplier": __subcategoryownedbysupplier,
}
