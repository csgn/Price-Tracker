import React, { useEffect, useState } from 'react';

import { Col, Container, Row } from 'react-bootstrap';

import ProductCard from './ProductCard';

import { fetchProducts } from './FetchProps';

export default function ProductList() {
  const [products, setProducts] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function run() {
      await fetchProducts(setProducts);
      setLoading(false);
    }
    run();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Container className="mt-5">
      <Row>
        {products?.length > 0 &&
          products?.map((product) => {
            return (
              <Col style={{ margin: '10px auto' }} key={product.productid}>
                {product.productid && <ProductCard product={product} />}
              </Col>
            );
          })}
      </Row>
    </Container>
  );
}
