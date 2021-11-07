from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Brand(Base):
    __tablename__ = "brand"

    brandid = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR, nullable=False)
    rateid = Column(Integer, ForeignKey("rate.rateid"), nullable=False)

    def __str__(self) -> str:
        return f"<Brand(brandid='{self.brandid}'', name='{self.name}'', url='{self.url}', rateid='{self.rateid}')>"

    def __repr__(self) -> str:
        return f"<Brand(BrandID(PK)='{self.brandid}', Name='{self.name}', URL='{self.url}', RateID(FK)='{self.rateid}')>"


class Rate(Base):
    __tablename__ = "rate"

    rateid = Column(Integer, primary_key=True)
    score = Column(Float)
    date = Column(TIMESTAMP, nullable=False)

    def __str__(self) -> str:
        return f"<Rate(rateid='{self.rateid}', score='{self.score}', date='{self.date}')>"

    def __repr__(self) -> str:
        return f"<Rate(RateID(PK)='{self.rateid}', Score='{self.score}', Date='{self.date}')>"


class Category(Base):
    __tablename__ = "category"

    categoryid = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    url = Column(Integer, ForeignKey(
        "subcategory.subcategoryid"), nullable=False)

    def __str__(self) -> str:
        return f"<Category(categoryid='{self.categoryid}', name='{self.name}', url='{self.url}')>"

    def __repr__(self) -> str:
        return f"<Category(CategoryID(PK)='{self.categoryid}', Name='{self.name}', URL='{self.url}')>"


class Subcategory(Base):
    __tablename__ = "subcategory"

    subcategoryid = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR, nullable=False)

    def __str__(self) -> str:
        return f"<Subcategory(subcategoryid='{self.subcategoryid}', name='{self.name}', url='{self.url}')>"

    def __repr__(self) -> str:
        return f"<Subcategory(SubcategoryID(PK)='{self.subcategoryid}', Name='{self.name}', URL='{self.url}')>"


class Supplier(Base):
    __tablename__ = "supplier"

    supplierid = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    url = Column(VARCHAR, nullable=False)
    rateid = Column(Integer, ForeignKey("rate.rateid"), nullable=False)

    def __str__(self) -> str:
        return f"<Supplier(supplierid='{self.supplierid}', name='{self.name}', url='{self.url}'), rate='{self.rateid}'>"

    def __repr__(self) -> str:
        return f"<Supplier(SupplierID(PK)='{self.supplierid}', Name='{self.name}', URL='{self.url}'), Rate(FK)='{self.rateid}'>"


class Price(Base):
    __tablename__ = "price"

    priceid = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=True)
    date = Column(TIMESTAMP, nullable=False)

    def __str__(self) -> str:
        return f"<Price(priceid='{self.priceid}', amount='{self.amount}', date='{self.date}')>"

    def __repr__(self) -> str:
        return f"<Price(PriceID(PK)='{self.priceid}', Amount='{self.amount}', Date='{self.date}')>"


class Product(Base):
    __tablename__ = "product"

    productid = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    images = Column(ARRAY(VARCHAR), nullable=True)
    rateid = Column(Integer, ForeignKey("rate.rateid"), nullable=False)
    priceid = Column(Integer, ForeignKey("price.priceid"), nullable=False)
    brandid = Column(Integer, ForeignKey("brand.brandid"), nullable=False)
    categoryid = Column(Integer, ForeignKey(
        "category.categoryid"), nullable=False)

    def __str__(self) -> str:
        return f"<Product(productid='{self.productid}', name='{self.name}', images='{self.images}', \
         rateid='{self.rateid}', priceid='{self.priceid}', brandid='{self.brandid}', categoryid='{self.categoryid}')>"

    def __repr__(self) -> str:
        return f"<Product(ProductID(PK)='{self.productid}', Name='{self.name}', Images='{self.images}', \
         RateID(FK)='{self.rateid}', PriceID(FK)='{self.priceid}', BrandID(FK)='{self.brandid}', CategoryID(FK)='{self.categoryid}')>"


class CategoryOwnedBySupplier(Base):
    __tablename__ = "categoryownedbysupplier"

    supplierid = Column(Integer, ForeignKey(
        "supplier.supplierid"), primary_key=True)
    categoryid = Column(Integer, ForeignKey(
        "category.categoryid"), primary_key=True)


class ProductOwnedBySupplier(Base):
    __tablename__ = "productownedbysupplier"

    supplierid = Column(Integer, ForeignKey(
        "supplier.supplierid"), primary_key=True)
    productid = Column(Integer, ForeignKey(
        "product.productid"), primary_key=True)


class SubcategoryOwnedBySupplier(Base):
    __tablename__ = "subcategoryownedbysupplier"

    supplierid = Column(Integer, ForeignKey(
        "supplier.supplierid"), primary_key=True)
    subcategoryid = Column(Integer, ForeignKey(
        "subcategory.subcategoryid"), primary_key=True)


class CategoryOwnedByBrand(Base):
    __tablename__ = "categoryownedbybrand"

    brandid = Column(Integer, ForeignKey("brand.brandid"), primary_key=True)
    categoryid = Column(Integer, ForeignKey(
        "category.categoryid"), primary_key=True)


class SubcategoryOwnedByBrand(Base):
    __tablename__ = "subcategoryownedbybrand"

    brandid = Column(Integer, ForeignKey("brand.brandid"), primary_key=True)
    subcategoryid = Column(Integer, ForeignKey(
        "subcategory.subcategoryid"), primary_key=True)


class ProductOwnedBySubcategory(Base):
    __tablename__ = "productownedbysubcategory"

    subcategoryid = Column(Integer, ForeignKey(
        "subcategory.subcategoryid"), primary_key=True)
    productid = Column(Integer, ForeignKey(
        "product.productid"), primary_key=True)
