import React from 'react';
import { Modal, Container, Row, Col } from 'react-bootstrap';

import ProductDetail from './ProductDetail';

export default function ProductModal(props) {
  return (
    <Modal show={props.show} onHide={props.onHide} fullscreen>
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.product.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          <ProductDetail {...props} />
        </Container>
      </Modal.Body>
      <Modal.Footer>
        <a
          href={'https://' + props.product.url}
          className="btn btn-outline-dark"
        >
          Go to Product Page
        </a>
      </Modal.Footer>
    </Modal>
  );
}
