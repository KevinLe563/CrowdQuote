import React from "react";
import {
	Chart as ChartJS,
	LineElement,
	TimeScale,
	LinearScale,
	PointElement,
	Title,
	Tooltip,
	Legend,
} from "chart.js";
import "chartjs-adapter-date-fns";
import { Line } from "react-chartjs-2";

import "./index.css";

import { ReactComponent as CloseButton } from "../../assets/imgs/x.svg";

ChartJS.register(
	LineElement,
	TimeScale,
	LinearScale,
	PointElement,
	Title,
	Tooltip,
	Legend
);

let populationData = {
	data: [],
};

let purpose = "Dance Room";
let address = "PAC, University Avenue West, Waterloo, ON, Canada";

const Modal = ({ open, onClose, position }) => {
	if (!open) return null;

	// goal: request to backend api to get populationData given (lat/lng)
	// current: mock static data for populationData
	populationData.data = [];
	let date = new Date();
	for (let i = 1; i <= 144; i++) {
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
		responsive: true,
		plugins: {
			title: {
				display: true,
				text: `CrowdQuote for ${address} in ${purpose}`,
			},
			legend: {
				display: false,
			},
		},
		scales: {
			x: {
				title: {
					display: true,
					text: "Date",
				},
				type: "time",
				time: {
					unit: "day",
				},
			},
			y: {
				title: {
					display: true,
					text: "Population",
				},
				beginAtZero: true,
			},
		},
	};

	return (
		<div className="modal-container">
			<div className="left-container">
				<div>
					<h1>{purpose}</h1>
					<h3>{address}</h3>

					<p>
						Latitude: {position.lat} | Longitude: {position.lng}
					</p>
				</div>
			</div>
			<div className="right-container">
				<CloseButton className="close-button" onClick={() => onClose()} />
				<div className="graph-container">
					<div className="graph">
						<Line data={data} options={options}></Line>
					</div>
					<p>Current Population: 23</p>
				</div>
			</div>
		</div>
	);
};

export default Modal;
