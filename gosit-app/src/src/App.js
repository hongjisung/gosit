import React, { Component } from 'react';
// import logo from './logo.svg';
import mainLogo from './gosit.png';
import './App.css';

// class App extends Component {
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <h1 className="App-title">Welcome to React</h1>
//         </header>
//         <p className="App-intro">
//           To get started, edit <code>src/App.js</code> and save to reload.
//         </p>
//       </div>
//     );
//   }
// }

class App extends Component {
  render() {
    return (
<div className="SearchApp">
    <img src={mainLogo} alt="" className="gosit-main-logo" />
    <div className="gosit-main-text">
    GoSit 앉아서가자
    </div>
    <div class="input-box">
        <input type="text" className="search-query" maxLength="17" />       
        <div className="search-btn">
            <i className="fa fa-angle-right"></i>
        </div>
    </div>
</div>
    );
  }
}


export default App;
