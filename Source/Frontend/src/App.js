import React from 'react';

import { BrowserRouter } from 'react-router-dom';

import Home from './components/Home';
import Navigator from './components/Navigator';

function App() {
  return (
    <div className="App">
      <Home />
      <BrowserRouter>
        <Navigator />
      </BrowserRouter>
    </div>
  );
}

export default App;
