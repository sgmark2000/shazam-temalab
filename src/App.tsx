import React, { MouseEventHandler } from 'react';
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import Button from 'react-bootstrap/Button'
import { Asd } from './asd';

function App() {
  const asd = () => { 
    alert("XD")
  }

  return (
    <div className="App">
      <header className='App-header'>
        <p>XD</p>
        <Asd></Asd>
      </header>
    </div>
  );
}

export default App;
