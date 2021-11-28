import React from 'react';

import { BrowserRouter } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';

import Home from './components/Home';
import Navigator from './components/Navigator';

function App() {
  return (
    <div className="App">
      <Container fluid>
        <Row className="m-4">
          <Col md={4} lg={3}>
            <Home />
          </Col>
          <Col md={8} lg={6}>
            <BrowserRouter>
              <Navigator />
            </BrowserRouter>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
