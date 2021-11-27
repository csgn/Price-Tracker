import React, { useState } from 'react';
import axios from 'axios';

import { ListGroup, ListGroupItem, Button, Spinner } from 'react-bootstrap';

export default function Navbar() {
  const [refreshActive, setRefreshActive] = useState();

  return (
    <ListGroup>
      <ListGroupItem>
        <a href="/">Home</a>
      </ListGroupItem>
      <ListGroupItem>
        <a href="/products">Products</a>
      </ListGroupItem>
      <ListGroupItem>
        <a href="/track">Track New Product</a>
      </ListGroupItem>
      <ListGroupItem>
        <Button
          disabled={refreshActive ? true : false}
          onClick={() => {
            setRefreshActive(true);
            axios
              .get('http://localhost:4444/refresh')
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
