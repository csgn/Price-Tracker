import React, { useEffect, useState } from 'react';

import { Card, Carousel, CarouselItem } from 'react-bootstrap';

import { fetchProductPrice } from './FetchProps';

export default function ProductCard(props) {
  const [product, setProduct] = useState([{}]);
  const [productPrice, setProductPrice] = useState([]);

  useEffect(() => {
    setProduct(props.product);
    fetchProductPrice(props.product.productid, setProductPrice);
  }, [props.product]);

  return (
    <Card style={{ width: '16rem' }}>
      <Card.Header
        style={{
          textAlign: 'center',
          color: '#555',
          border: 'none',
          backgroundColor: 'white',
        }}
      >
        {product.name?.length > 56
          ? product.name?.slice(0, 56) + '...'
          : product.name}
      </Card.Header>

      <Card.Body style={{ textAlign: 'center' }}>
        <Carousel variant="dark">
          {product.images !== undefined &&
            product.images.map((img) => {
              return (
                <CarouselItem>
                  <Card.Img src={img}></Card.Img>
                </CarouselItem>
              );
            })}
        </Carousel>
        <Card.Text>
          <span>{productPrice[0]?.amount} </span>
          <i>TL</i>
        </Card.Text>
        <a
          href={`/products/${product.productid}/`}
          className="btn btn-outline-dark"
        >
          Visit The Product Page
        </a>
      </Card.Body>
    </Card>
  );
}
