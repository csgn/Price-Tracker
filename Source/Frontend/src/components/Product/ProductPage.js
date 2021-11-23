import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';

import {
  fetchProduct,
  fetchProductPrice,
  fetchProductSupplier,
  fetchProductBrand,
  fetchProductCategory,
  fetchProductSubcategory,
} from './FetchProps';

export default function ProductPage() {
  const [product, setProduct] = useState({});
  const [productPrice, setProductPrice] = useState([{}]);
  const [productSupplier, setProductSupplier] = useState([{}]);
  const [productCategory, setProductCategory] = useState([{}]);
  const [productSubcategory, setProductSubcategory] = useState([{}]);
  const [productBrand, setProductBrand] = useState([{}]);

  const { productid } = useParams();

  useEffect(() => {
    fetchProduct(productid, setProduct);
    fetchProductPrice(productid, setProductPrice);
    fetchProductSupplier(productid, setProductSupplier);
    fetchProductBrand(productid, setProductBrand);
    fetchProductCategory(productid, setProductCategory);
    fetchProductSubcategory(productid, setProductSubcategory);
  }, []);

  return (
    <div>
      {productCategory && (
        <div>
          <ul>
            <li>
              <a href={productCategory.url}>{productCategory.name}</a>
            </li>
            {productSubcategory.length > 0 &&
              productSubcategory.map((subcategory) => {
                return (
                  <li>
                    <a href={subcategory.url}>{subcategory.name}</a>
                  </li>
                );
              })}
          </ul>
        </div>
      )}

      {product.productid && (
        <div>
          <h4>{product.name}</h4>
          <p>{product.rate}</p>
          <p>
            <a href={productBrand.url}>{productBrand.name}</a>
          </p>
          <p>
            <a href={product.url}>GO TO PRODUCT</a>
          </p>
          <ul>
            {product.images.map((img) => {
              return (
                <p>
                  <img src={img} width={256} height={256} />
                </p>
              );
            })}
          </ul>
        </div>
      )}

      {productPrice.length > 0 && productSupplier.length > 0 && (
        <div>
          {productSupplier.map((supplier) => {
            return (
              <div style={{ border: '1px black solid', margin: '10px auto' }}>
                <p>{supplier.name}</p>
                <p>{supplier.rate}</p>
                <ul>
                  {productPrice.map((price) => {
                    if (price.supplierid === supplier.supplierid) {
                      return (
                        <li>
                          <p>{price.amount}</p>
                          <p>{price.startdate}</p>
                        </li>
                      );
                    }
                  })}
                </ul>
                <a href={supplier.url}>GO TO SUPPLIER PAGE</a>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
