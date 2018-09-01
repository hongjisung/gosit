import React, { Component } from 'react';
import img_landing_logo from '../img/gosit_landing.png';
import './landing.css';


class LandingPage extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      searchQuery: ''
    }

    this.busDataHTML = "";
    }


    /* Detect Enter Keypress from Input Text, and link */
    _handleKeyPress = (e) => {
        if(e.key === 'Enter') {
          this.props.loadBusPage(this.state.searchQuery);
        }
    }

    /* Dynamically Update state['input_query'] by Input text */
    _handleInputChange = (e) => {
        this.state.searchQuery = e.target.value;
    }




    render() {
        return(
          <div className="LandingPage">
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
                       onChange={this._handleInputChange}
                       />
                <i className="fa fa-angle-right search-btn" id="search-btn"
                   onClick={this.loadBusPage}/>
              </div>
            </div>
          </div>
        )
    }
}

export default LandingPage;