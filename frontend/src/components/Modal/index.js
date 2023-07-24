import React, { useEffect, useState } from "react";
import axios from "axios";
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

// let purpose = "Dance Room";
// let address = "PAC, University Avenue West, Waterloo, ON, Canada";

const Modal = ({ open, onClose, position }) => {
	const [address, setAddress] = useState();
	const [purpose, setPurpose] = useState();
	const [populationData, setPopulationData] = useState();

	const fetchData = async () => {
		await axios
			.get("http://localhost:8000/api/location/", {
				params: {
					lat: 80.788,
					lng: 45.34,
					// lat: position.lat,
					// lng: position.lng,
				},
			})
			.then((res) => {
				console.log(res);
				const data = res.data;

				axios
					.get("http://localhost:8000/api/population/", {
						params: {
							location_id: data.id,
						},
					})
					.then((res) => {
						console.log(res);
						setPopulationData(res.data);
					})
					.catch(() => console.log("Get Population Data Fail"));

				setAddress(
					`${data.civic_number} ${data.street_name} ${data.postal_code}`
				);
				setPurpose(`${data.building_name} ${data.room}`);
			})
			.catch(() => console.log("Get Location Fail"));
	};

	useEffect(() => {
		if (!open) return () => {};

		fetchData();
		const interval = setInterval(fetchData, 10000);

		return () => clearInterval(interval);
	}, [open]);

	if (!open) {
		return null;
	}

	if (!address || !purpose || !populationData) return null;

	// console.log(address);
	// console.log(purpose);
	// console.log(populationData);

	// goal: request to backend api to get populationData given (lat/lng)
	// current: mock static data for populationData
	// populationData.data = [];
	// let date = new Date();
	// for (let i = 1; i <= 144; i++) {
	// 	populationData.data.push({
	// 		location_id: i,
	// 		people_count: Math.floor(Math.random() * 100),
	// 		date_time: date,
	// 	});
	// 	date = new Date(date.setMinutes(date.getMinutes() + 10));
	// }

	console.log("pop data", populationData);
	// console.log(populationData.data.map((obj) => obj.date_time));

	const data = {
		// labels: ["2022-11-01", "2022-11-02", "2022-11-03", "2022-11-04"],
		labels: populationData.map((obj) => obj.timestamp),
		datasets: [
			{
				label: "people",
				data: populationData.map((obj) => obj.people_count),
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
