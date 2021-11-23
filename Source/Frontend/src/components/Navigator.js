/* eslint-disable no-unused-vars */
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Home from './Home';

import ProductList from './Product/ProductList';
import ProductPage from './Product/ProductPage';

class Navigator extends React.Component {
  render() {
    return (
      <div>
        <Routes>
          <Route
            path={`/products/:productid`}
            element={<ProductPage />}
          ></Route>

          <Route path="/products" element={<ProductList />}></Route>

          <Route exact path="/" element={<Home />}></Route>
        </Routes>
      </div>
    );
  }
}

export default Navigator;
