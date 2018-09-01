import React, { Component } from 'react';
import "./gosit.css";
import LandingPage from './landing';
import BusPage from './bus';
import axios from 'axios';

class Gosit extends Component {
  constructor(props)
  {
    super(props);
    this.state = {
      page: 'landing',
      busName: '',
      busRoute: ''
    }

    this.busDataHTML = "";
  }

  getBusData = () => {
    return this.state;
  }

  loadBusPage = (busName) => {
    axios.get('http://35.229.154.169/initialCall', {
      params: {
        busName: busName
      }
    })
      .then(res => {
        var response = JSON.parse(res.request.response);
        if(response.status == true) {
          this.setState({
            busName: response.busName,
            busId: response.busId,
            busRoute: response.busRoute
          })
        }
        this.setState({
          page: 'bus'
        });
    });

  }

  render()
  {
    switch(this.state.page)
    {
      case 'landing':
        return <LandingPage loadBusPage={this.loadBusPage} />
      case 'bus':
        return <BusPage getBusData={this.getBusData}
               />
      default:
        return <div />
    }
  }

}
 
export default Gosit;