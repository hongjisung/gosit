import React, { Component } from 'react';
import "./gosit.css";
import img_landing_logo from '../img/gosit_landing.png';

var LineChart = require("react-chartjs").Line;


class Gosit extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      page: 'landing',
      input_query: '',
      bus: ''
    }

    this.busDataHTML = "";
  }

  render()
  {
    return(
      <div className="container-main">
        <div className="TopContainer">
          <div className="LogoHolder">
            <img src={img_landing_logo} />
          </div>
          <div className="SearchHolder">
            <div className="title">
            Go Sit : 앉아서 가자
            </div>
            <div className="description">
            서울 버스별 승하차 인원 분석 툴
            </div>
            <input type="text"
                   className="search-input"
                   maxLength="22"
                   placeholder="오늘도 바쁘게 사는 당신이 타고 갈 버스 번호는?"
                   onKeyPress={this._handleKeyPress}
                   onChange={this._handleSearchInputChange}
                   />
            <i className="fa fa-angle-right search-btn" id="search-btn"
               onClick={this.loadBusPage}/>
          </div>
        </div>
        <div className="BusDataHolder">
        </div>
      </div>
    )
  }

  /* Dynamically Update state['input_query'] by Input text */
  _handleSearchInputChange = (e) => {
    this.state.input_query = e.target.value;
  }

  /* Detect Enter Keypress from Input Text, and link */
  _handleKeyPress = (e) => {
    if(e.key === 'Enter') {
      this.loadBusPage();
    }
  }

  /* Load Bus Page */
  loadBusPage = () => {
    this.busName = this.state.input_query;
    alert(this.busName);
  }
}
 
export default Gosit;