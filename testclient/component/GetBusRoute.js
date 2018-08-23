import React, {Component} from 'react';
import axios from 'axios';

class GetBusRoute extends Component{
    state = {
        key : [],
        busRoute : [],
        routeNum : '',
    }


    handleChange = (e)=>{
        this.setState({
            routeNum : e.target.value
        });

        let getData = axios.get('http://localhost:5000/busRoute',{
                params: {
                    routeNum : e.target.value
                },
            }
        );
        

        getData.then( response =>{
            let routes = [];
            let keys = [];
            for (let key in response.data){
                let route = response.data[key];
                let route_data = [];
                for(let key2 in route){
                    route_data = route_data.concat(route[key2]);
                }
                keys = Object.keys(route);
                routes = routes.concat([route_data]);
            }
            this.setState({
                key : keys,
                busRoute : routes
            });
        });
    }



    render(){
        const style={
            border: '1px solid black',
            padding: '8px',
            margin: '8px'
        };
        const {key, busRoute} = this.state;
        const keylist = key.map(
            k => (
                <th>{k}</th>
            )
        );
        const routelist = busRoute.map(
            routeinfo => (
                routeinfo.map(
                    data =>(
                        <th>{data}</th>
                    )
                )
            )
        );

        const busroutelist = routelist.map(
            info =>(
                <tr>{info}</tr>
            )
        );


        return(
            <div>
                <input  style = {style}
                    placeholder='input bus route Number'
                    onChange={this.handleChange}
                />
                <p>{this.state.routeNum}</p>
                <thead><tr>{keylist}</tr></thead>
                <tbody>{busroutelist}</tbody>
            </div>
        );
    }
}

export default GetBusRoute;