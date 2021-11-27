import React from 'react';
import { Modal, Container, Row, Col } from 'react-bootstrap';
import ProductCarousel from './ProductCarousel';

import ProductDetail from './ProductDetail';

export default function ProductModal(props) {
  return (
    <Modal show={props.show} onHide={props.onHide} size="lg" fullscreen>
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.product.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          <Row>
            <Col xs={6} md={4}>
              <ProductCarousel images={props.product.images} />
            </Col>
            <Col xs={12} md={8}>
              <ProductDetail {...props} />
            </Col>
          </Row>
          <Row></Row>
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
