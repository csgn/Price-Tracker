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
    URL varchar(255) not null UNIQUE,
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
    URL varchar(255) not null UNIQUE,
    PRIMARY KEY (BrandID)
);
"""

__supplier = """
CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID serial,
    Name varchar(255) not null,
    Rate float,
    URL varchar(255) not null UNIQUE,
    PRIMARY KEY (SupplierID)
);
"""

__product = """
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
"""

__price = """
CREATE TABLE IF NOT EXISTS Price (
    PriceID serial,
    Amount float,
    StartDate timestamp not null default now(),
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (PriceID)
);
"""


__categoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS CategoryOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    categoryid int REFERENCES category ON DELETE CASCADE,
    PRIMARY KEY (supplierid, categoryid)
);
"""

__categoryownedbybrand = """
CREATE TABLE IF NOT EXISTS CategoryOwnedByBrand (
    brandid int REFERENCES brand ON DELETE CASCADE,
    categoryid int REFERENCES category ON DELETE CASCADE,
    PRIMARY KEY (brandid, categoryid)
);
"""

__productownedbysupplier = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (supplierid, productid)
);
"""

__subcategoryownedbysupplier = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    PRIMARY KEY (supplierid, subcategoryid)
);
"""

__productownedbysubcategory = """
CREATE TABLE IF NOT EXISTS ProductOwnedBySubcategory (
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    productid int REFERENCES product ON DELETE CASCADE,
    PRIMARY KEY (subcategoryid, productid)
);
"""

__subcategoryownedbybrand = """
CREATE TABLE IF NOT EXISTS SubcategoryOwnedByBrand (
    brandid int REFERENCES brand ON DELETE CASCADE,
    subcategoryid int REFERENCES subcategory ON DELETE CASCADE,
    PRIMARY KEY (brandid, subcategoryid)
);
"""

__brandownedbysupplier = """
CREATE TABLE IF NOT EXISTS BrandOwnedBySupplier (
    supplierid int REFERENCES supplier ON DELETE CASCADE,
    brandid int REFERENCES brand ON DELETE CASCADE,
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
