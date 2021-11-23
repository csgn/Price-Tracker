import React from 'react';

import { Container, ListGroup, ListGroupItem } from 'react-bootstrap';

import Navbar from './Navbar/Navbar';

class Home extends React.Component {
  render() {
    return (
      <Container>
        <Navbar />
      </Container>
    );
  }
}

export default Home;
