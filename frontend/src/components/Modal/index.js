import React from "react";
import {
	Chart as ChartJS,
	LineElement,
	TimeScale,
	LinearScale,
	PointElement,
	Tooltip,
	Legend,
} from "chart.js";
import "chartjs-adapter-date-fns";
import { Line } from "react-chartjs-2";

import "./index.css";

ChartJS.register(
	LineElement,
	TimeScale,
	LinearScale,
	PointElement,
	Tooltip,
	Legend
);

let populationData = {
	data: [],
};

const Modal = ({ open, onClose, position }) => {
	if (!open) return null;

	// goal: request to backend api to get populationData given (lat/lng)
	// current: mock static data for populationData
	populationData.data = [];
	let date = new Date();
	for (let i = 1; i <= 100; i++) {
		populationData.data.push({
			location_id: i,
			people_count: Math.floor(Math.random() * 100),
			date_time: date,
		});
		date = new Date(date.setMinutes(date.getMinutes() + 10));
	}

	console.log(populationData);
	// console.log(populationData.data.map((obj) => obj.date_time));

	const data = {
		// labels: ["2022-11-01", "2022-11-02", "2022-11-03", "2022-11-04"],
		labels: populationData.data.map((obj) => obj.date_time),
		datasets: [
			{
				label: "people",
				data: populationData.data.map((obj) => obj.people_count),
				backgroundColor: "aqua",
				borderColor: "black",
				tension: 0.4,
			},
		],
	};

	const options = {
		scales: {
			x: {
				type: "time",
				time: {
					unit: "day",
				},
			},
			y: {
				beginAtZero: true,
			},
		},
	};

	// geocoding (lat/long -> address) or we can get from db response

	return (
		<div className="modal-container">
			<p>
				Address | Latitude: {position.lat} | Longitude: {position.lng}
			</p>
			<p>Current Population: 23</p>
			<div className="graph">
				<Line data={data} options={options}></Line>
			</div>
			<button onClick={() => onClose()}>Close</button>
		</div>
	);
};

export default Modal;
