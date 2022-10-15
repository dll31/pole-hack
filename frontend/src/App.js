import './App.css';
import React, { useEffect, useState, useRef } from 'react';
import axios from "axios";
import MyLineChart from './lineChartComponent';


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
			} catch (error) {
			console.log(error);
			}

			try {
				const res = await axios.get('/plot_an_data');
				setAnData(anData => [...anData, res.data]);
			} catch (error) {
				console.log(error);
			}

		};

		const id = setInterval(() => {
		  fetchData(); 
		}, 200);
	  
		fetchData();
	  
		return () => clearInterval(id);
	}, [])


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
					<img src="/video_feed" alt="video" width='1080' height='720'/>
				</div>
				
				<div className='plots'>
				<div className='plot'>
					<MyLineChart chart={{data: data}}/>
				</div>

				<div className='plot'>
					<MyLineChart chart={{data: anData}}/>
				</div>
				</div>
				
			</div>

			

			{/* <div className="dateTime">
				{date}
			</div> */}
		

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
	);
}

export default App;
