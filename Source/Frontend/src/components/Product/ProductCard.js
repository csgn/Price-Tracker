import React, { useEffect, useState } from 'react';

import { Card, Button } from 'react-bootstrap';

import {
  fetchProductPrice,
  fetchProductSupplier,
  fetchProductCategory,
  fetchProductSubcategory,
  fetchProductBrand,
} from './FetchProps';
import ProductCarousel from './ProductCarousel';
import ProductModal from './ProductModal';

export default function ProductCard(props) {
  const [loading, setLoading] = useState(true);
  const [product, setProduct] = useState();
  const [productPrice, setProductPrice] = useState();
  const [productSupplier, setProductSupplier] = useState();
  const [productCategory, setProductCategory] = useState();
  const [productSubcategory, setProductSubcategory] = useState();
  const [productBrand, setProductBrand] = useState();
  const [productModalShow, setProductModalShow] = useState(false);

  useEffect(async () => {
    setProduct(props.product);
    async function run() {
      await fetchProductPrice(props.product.productid, setProductPrice);
      await fetchProductSupplier(props.product.productid, setProductSupplier);
      await fetchProductBrand(props.product.productid, setProductBrand);
      await fetchProductCategory(props.product.productid, setProductCategory);
      await fetchProductSubcategory(
        props.product.productid,
        setProductSubcategory
      );

      setLoading(false);
    }

    run();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Card style={{ width: '15rem' }}>
      <Card.Header
        style={{
          textAlign: 'center',
          color: '#555',
          border: 'none',
          backgroundColor: 'white',
        }}
      >
        {product?.name?.length > 32
          ? product?.name?.slice(0, 32) + '...'
          : product?.name}
      </Card.Header>

      <Card.Body style={{ textAlign: 'center' }}>
        <ProductCarousel images={product?.images} />
      </Card.Body>
      <Card.Footer style={{ border: 'none' }}>
        <Card.Text className="text-center">
          <span>{productPrice[0]?.amount} </span>
          <i>TL</i>
        </Card.Text>
        <center>
          <Button
            variant="outline-dark "
            onClick={() => setProductModalShow(true)}
          >
            Show the Product
          </Button>
        </center>
        <ProductModal
          show={productModalShow}
          onHide={() => setProductModalShow(false)}
          product={product}
          price={productPrice}
          supplier={productSupplier}
          brand={productBrand}
          category={productCategory}
          subcategory={productSubcategory}
        />
      </Card.Footer>
    </Card>
  );
}
