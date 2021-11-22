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

__price = """
CREATE TABLE IF NOT EXISTS Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null default now(),
    supplierid int REFERENCES supplier,
    productid int REFERENCES product,
    PRIMARY KEY (PriceID)
);
"""


__categoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS CategoryOwnedBySupplier (
    supplierid int REFERENCES supplier,
    categoryid int REFERENCES category,
    PRIMARY KEY (supplierid, categoryid)
);
"""

__categoryownedbybrand = """
CREATE TABLE IF NOT EXISTS CategoryOwnedByBrand (
    brandid int REFERENCES brand,
    categoryid int REFERENCES category,
    PRIMARY KEY (brandid, categoryid)
);
"""

__productownedbysupplier = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySupplier (
    supplierid int REFERENCES supplier,
    productid int REFERENCES product,
    PRIMARY KEY (supplierid, productid)
);
"""

__subcategoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedBySupplier (
    supplierid int REFERENCES supplier,
    subcategoryid int REFERENCES subcategory,
    PRIMARY KEY (supplierid, subcategoryid)
);
"""

__productownedbysubcategory = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySubcategory (
    subcategoryid int REFERENCES subcategory,
    productid int REFERENCES product,
    PRIMARY KEY (subcategoryid, productid)
);
"""

__subcategoryownedbybrand = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedByBrand (
    brandid int REFERENCES brand,
    subcategoryid int REFERENCES subcategory,
    PRIMARY KEY (brandid, subcategoryid)
);
"""

__brandownedbysupplier = """
CREATE TABLE IF NOT EXISTS BrandOwnedBySupplier (
    supplierid int REFERENCES supplier,
    brandid int REFERENCES brand,
    PRIMARY KEY (supplierid, brandid)
);
"""

STATIC_TABLES = {
    "Category": __category,
    "Subcategory": __subcategory,
    "Brand": __brand,
    "Supplier": __supplier,
    "Product": __product,
    "Price": __price,
    "CategoryOwnedBySupplier": __categoryownedbysupplier,
    "CategoryOwnedByBrand": __categoryownedbybrand,
    "ProductOwnedBySupplier": __productownedbysupplier,
    "ProductOwnedBySubcategory": __productownedbysubcategory,
    "SubcategoryOwnedByBrand": __subcategoryownedbybrand,
    "SubcategoryOwnedBySupplier": __subcategoryownedbysupplier,
    "BrandOwnedBySupplier": __brandownedbysupplier,
}
