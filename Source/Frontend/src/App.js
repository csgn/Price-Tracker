import React from 'react';

import { BrowserRouter } from 'react-router-dom';

import Navigator from './components/Navigator';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navigator />
      </BrowserRouter>
    </div>
  );
}

export default App;
