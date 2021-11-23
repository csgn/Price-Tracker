import React, { useEffect, useState } from 'react';

import { Col, Container, Row } from 'react-bootstrap';

import ProductCard from './ProductCard';

import { fetchProducts } from './FetchProps';

export default function ProductList() {
  const [products, setProducts] = useState([{}]);

  useEffect(() => {
    fetchProducts(setProducts);
  }, []);

  return (
    <Container>
      <Row>
        {products?.length > 0 &&
          products?.map((product) => {
            return (
              <Col style={{ margin: '10px auto' }}>
                <ProductCard product={product} />
              </Col>
            );
          })}
      </Row>
    </Container>
  );
}
