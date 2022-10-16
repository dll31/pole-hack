import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './App.css';



const MyLineChart = (props) => {
    return (
    <div>
        <div className='title'>
        {props.chart.title}
        </div>
        <LineChart
        width={500}
        height={320}
        data={props.chart.data}
        margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
        }}
        >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={props.chart.xaxis} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey={props.chart.line} stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
            <button 
                className='plot_btn'
                onClick={() => props.chart.onClear([])}>
                    Clear plot
                </button>
        </div>
    )
};


export default MyLineChart;
  