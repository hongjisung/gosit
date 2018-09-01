import React, {Component} from 'react';
import {Line} from 'react-chartjs-2';
import img_landing_logo from '../img/gosit_landing.png';
import './bus.css';


class BusPage extends Component {
    constructor(props)
  {
    super(props);
    this.state = {
      searchQuery: '',
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
    _handleSearchInputChange = (e) => {
        this.setState({searchQuery: e.target.value});
    }

    createChart() {
        var data = {
            labels: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
            datasets: [
                {
                    label: "주말 / 공휴일",
                    fillColor: "rgba(0,0,0,0)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "rgba(0,0,0,0)",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: [660, 41, 0, 0, 234, 874, 1362, 2774, 3807, 2789, 
                        2275, 2241, 2460, 2696, 2615, 2864, 3115, 3522, 4188, 3275, 2488, 2437,
                        2285, 1490]
                }, {
                    label: "평일",
                    fillColor: "rgba(0,0,0,0)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "rgba(0,0,0,0)",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: [519, 32, 0, 0, 184, 688, 1072, 2183, 2996, 2195, 1791, 1936, 2122, 2058, 2254, 2452, 2773, 3296, 2578, 1958, 1918, 1799, 1173]
                }
            ]
        };
        var options = {
            scales: {
                xAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                            }
                        }],
                yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                            }   
                        }]
                },
            ///Boolean - Whether grid lines are shown across the chart
            scaleShowGridLines : false,

            //Boolean - Whether to show horizontal lines (except X axis)
            scaleShowHorizontalLines: false,

            //Boolean - Whether to show vertical lines (except Y axis)
            scaleShowVerticalLines: false,

            //Boolean - Whether the line is curved between points
            bezierCurve : true,

            //Number - Tension of the bezier curve between points
            bezierCurveTension : 0.4,

            //Boolean - Whether to show a dot for each point
            pointDot : true,

            //Number - Radius of each point dot in pixels
            pointDotRadius : 4,

            //Number - Pixel width of point dot stroke
            pointDotStrokeWidth : 1,

            //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
            pointHitDetectionRadius : 20,

            //Boolean - Whether to show a stroke for datasets
            datasetStroke : true,

            //Number - Pixel width of dataset stroke
            datasetStrokeWidth : 2,

            //Boolean - Whether to fill the dataset with a colour
            datasetFill : true,
            
            //Boolean - Whether to horizontally center the label and point dot inside the grid
            offsetGridLines : false
        };;
        return (
            <Line data={data} options={options} className="stat-chart" />
        )
    }


    createStationHTML() {
        console.log(this.busRoute)
        console.log(this.state.busRoute)
        // var stationHTMLs = [this.busRoute].map((route) =>
        //     <div className="station">
        //         <div className="station-index">
        //             {this.route.routeOrder}
        //         </div>
        //         <div className="line" />
        //         <div className="circle" />
        //         <div className="station-name">
        //             {route.stationName}
        //         </div>
        //     </div>
        //     )

        return (<div></div>)
    
    }

    render() {
        return(
            <div className="BusPage">
                <div className="top-holder">
                    <img src={img_landing_logo} />
                </div>
                {/* <div className="chart-holder"> */}
                {/*     {this.createChart()} */}
                {/* </div> */}

                <div className="stats-holder">
                    
                </div>
                <div className="station-holder">
                    {this.createStationHTML()}
                </div>
            </div>
        )
    }
}

export default BusPage;