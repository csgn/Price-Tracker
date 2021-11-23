import React from 'react';
import { ListGroup, ListGroupItem } from 'react-bootstrap';

export default function Navbar() {
  return (
    <ListGroup>
      <ListGroupItem>
        <a href="/">Home</a>
      </ListGroupItem>
      <ListGroupItem>
        <a href="/products">Products</a>
      </ListGroupItem>
    </ListGroup>
  );
}
