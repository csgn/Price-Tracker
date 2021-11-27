import React from 'react';

import { Container } from 'react-bootstrap';

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
