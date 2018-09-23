import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Layout from "./js/components/layout/Layout";

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="bg-dark" style={{height:'5.3rem'}}>
          {/*<img src={logo} className="App-logo" alt="logo" />*/}
          <h1 className="text-white text-center" style={{paddingTop:'1rem'}}>Video Silence Remover 9001!</h1>
        </header>
          <Layout/>
      </div>
    );
  }
}

export default App;
