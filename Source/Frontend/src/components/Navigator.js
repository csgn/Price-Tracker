/* eslint-disable no-unused-vars */
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import ProductList from './Product/ProductList';
import TrackPage from './TrackPage';

class Navigator extends React.Component {
  render() {
    return (
      <div>
        <Routes>
          <Route path="/track" element={<TrackPage />}></Route>

          <Route path="/products" element={<ProductList />}></Route>

          <Route exact path="/"></Route>
        </Routes>
      </div>
    );
  }
}

export default Navigator;
