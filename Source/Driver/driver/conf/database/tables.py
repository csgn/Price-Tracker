__category = """
CREATE TABLE IF NOT EXISTS Category (
    CategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    PRIMARY KEY (CategoryID)
);
"""
__subcategory = """
CREATE TABLE IF NOT EXISTS Subcategory (
    SubcategoryID serial,
    Name varchar(255) not null,
    URL varchar(255) not null,
    CategoryID int not null,
    PRIMARY KEY (SubcategoryID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID)
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
    Rate float,
    URL varchar(255) not null,
    PRIMARY KEY (SupplierID)
);
"""

__price = """
CREATE TABLE IF NOT EXISTS Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null,
    SupplierID int not null,
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    PRIMARY KEY (PriceID)
);
"""

__product = """
CREATE TABLE IF NOT EXISTS Product (
    ProductID serial,
    Name varchar(255) not null,
    Images varchar(255) array,
    Rate float,
    URL varchar(255) not null,
    BrandID int not null,
    CategoryID int not null,
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID),
    PRIMARY KEY (ProductID)
);
"""

__categoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS CategoryOwnedBySupplier (
    SupplierID int not null,
    CategoryID int not null,
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier(SupplierID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID),
    PRIMARY KEY (SupplierID, CategoryID)
);
"""

__categoryownedbybrand = """
CREATE TABLE IF NOT EXISTS CategoryOwnedByBrand (
    BrandID int not null,
    CategoryID int not null,
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    FOREIGN KEY (CategoryID)
        REFERENCES Category (CategoryID),
    PRIMARY KEY (BrandID, CategoryID)
);
"""

__productownedbysupplier = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySupplier (
    SupplierID int not null,
    ProductID int not null,
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    PRIMARY KEY (SupplierID, ProductID)
);
"""

__subcategoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedBySupplier (
    SupplierID int not null,
    SubcategoryID int not null,
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID),
    PRIMARY KEY (SupplierID, SubcategoryID)
);
"""

__productownedbysubcategory = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySubcategory (
    SubcategoryID int not null,
    ProductID int not null,
    FOREIGN KEY (ProductID)
        REFERENCES Product (ProductID),
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID),
    PRIMARY KEY (SubcategoryID, ProductID)
);
"""

__subcategoryownedbybrand = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedByBrand (
    BrandID int not null,
    SubcategoryID int not null,
    FOREIGN KEY (SubcategoryID)
        REFERENCES Subcategory (SubcategoryID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    PRIMARY KEY (BrandID, SubcategoryID)
);
"""

__brandownedbysupplier = """
CREATE TABLE IF NOT EXISTS BrandOwnedBySupplier (
    SupplierID int not null,
    BrandID int not null,
    FOREIGN KEY (SupplierID)
        REFERENCES Supplier (SupplierID),
    FOREIGN KEY (BrandID)
        REFERENCES Brand (BrandID),
    PRIMARY KEY (SupplierID, BrandID)
);
"""

STATIC_TABLES = {
    "Category": __category,
    "Subcategory": __subcategory,
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
    "BrandOwnedBySupplier": __brandownedbysupplier,
}
