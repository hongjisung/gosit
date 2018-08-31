import React, { Component } from 'react';
import "./gosit.css";
import img_landing_logo from '../img/gosit_landing.png';

class Gosit extends Component {
  render() 
  {
    return (
      <div className="landing-container">
        <LogoHolder />
        <SearchHolder />
      </div>
      );
  }
}

class LogoHolder extends Component {
  render()
  {
    return (
      <div className="LogoHolder">
        <img src={img_landing_logo} />
      </div>
      )
  }
}

class SearchHolder extends Component{
  render()
  {
    return (
      <div className="SearchHolder">
          <div className="title">
            Go Sit : 앉아서 가자
          </div>
          <div className="description">
            서울 버스별 승하차 인원 분석 툴
          </div>
          <input type="text"
                 className="search-input"
                 maxlength="22"
                 placeholder="오늘 그대가 타고갈 버스는?"/>
          <i class="fa fa-angle-right search-btn"></i>
      </div>
      )
  }
}

export default Gosit;