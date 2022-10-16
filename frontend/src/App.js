import './App.css';
import React, { useEffect, useState, useRef } from 'react';
import axios from "axios";
import MyLineChart from './lineChartComponent';
import MyPercentAreaChart from './percentAreaChartComponent';


function App() {

	const [data, setData] = useState([]);
	const [anData, setAnData] = useState([]);

	const [maxNonOversizedOre, setMaxNonOversizedOre] = useState(250)
	const [tempMaxNonOversizedOre, setTempMaxNonOversizedOre] = useState(250)
	const inputRef = useRef();

	useEffect(() => {
		const fetchData = async () => {
			try {
			const res = await axios.get('/plot_data');
			setData(data => [...data, res.data]);
			// console.log(data);
			} catch (error) {
			console.log(error);
			}

			try {
				const res = await axios.get('/plot_an_data');
				setAnData(anData => [...anData, res.data]);
				// console.log(anData);
			} catch (error) {
				console.log(error);
			}

		};

		const id = setInterval(() => {
		  fetchData(); 
		}, 2000);
	  
		fetchData();
	  
		return () => clearInterval(id);
	}, [])


	const updateData = (state) => {
		setData(state);
	}

	const updateAnData = (state) => {
		setAnData(state);
	}

	const rrr = () => {

	}


	const handlePostQuery = (query) => {

		query.preventDefault()
		setTempMaxNonOversizedOre(maxNonOversizedOre)
		inputRef.current.value = ""

		var myParams = {
			data: maxNonOversizedOre
		}

		if (query != "") {
			axios.post('/api/query', myParams)
				.then(function(response){
					console.log(response);
		   //Perform action based on response
			})
			.catch(function(error){
				console.log(error);
		   //Perform action based on error
			});
		}
	}	

	return (
		<div className="App">
			<div className='mainBody'>


				<div className="stream">
					<img className='video' src="/video_feed" alt="video"/>
					<div className="OperatorFields">
						<form>
							<p>Now ore limit is: {tempMaxNonOversizedOre}</p>

							
							<input 
								ref={inputRef}
								type="text"
								onChange={event => setMaxNonOversizedOre(event.target.value)}
							>
								
							</input>

							<button onClick={handlePostQuery}>Set ore limit</button>

						</form>
					</div>
				</div>
				
				<div className='plots'>
				<div className='plot'>
					<MyPercentAreaChart chart={{data: data}} /> 
				</div>

				<div className='plot' >
					<MyLineChart chart={{data: anData, onClear: updateAnData, title: "Title2", xaxis: "time", line: "max_size"}}/>
				</div>
				</div>
				
			</div>

			

			{/* <div className="dateTime">
				{date}
			</div> */}
		

			

		</div>
	);
}

export default App;
