import React, { useState } from 'react';
import axios from 'axios';

import { ListGroup, ListGroupItem, Button, Spinner } from 'react-bootstrap';

export default function Navbar() {
  const [refreshActive, setRefreshActive] = useState();

  return (
    <ListGroup>
      <ListGroupItem style={{ border: 'none', fontSize: '32px' }}>
        <a href="/products" className="text-secondary">
          Home
        </a>
      </ListGroupItem>
      <ListGroupItem style={{ border: 'none', fontSize: '32px' }}>
        <a href="/products" className="text-secondary">
          Products
        </a>
      </ListGroupItem>
      <ListGroupItem style={{ border: 'none', fontSize: '32px' }}>
        <a href="/track" className="text-secondary">
          Track New Product
        </a>
      </ListGroupItem>
      <ListGroupItem style={{ border: 'none', fontSize: '32px' }}>
        <Button
          variant="outline-dark"
          disabled={refreshActive ? true : false}
          onClick={() => {
            setRefreshActive(true);
            axios
              .post('http://localhost:5000/refresh')
              .then((res) => {
                console.log(res);
              })
              .catch((err) => {
                console.error(err);
              })
              .finally(() => {
                setRefreshActive(false);
              });
          }}
        >
          <span className="p-2">Refresh</span>
          {refreshActive && (
            <Spinner animation="border" role="status" size="sm"></Spinner>
          )}
        </Button>
      </ListGroupItem>
    </ListGroup>
  );
}
