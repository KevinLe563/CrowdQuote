import React, { useState } from "react";
import { Scatter } from "react-chartjs-2";
import CloseButton from "../../assets/imgs/x.svg";
import "./index.css";

import backgroundImage from "../../assets/imgs/layout.jpg";

interface ModalProps {
	open?: boolean;
	onClose: () => void;
	populationData: any;
	point: any;
}

const ClusterModal: React.FC<ModalProps> = ({
	open,
	onClose,
	populationData,
	point,
}) => {
	if (!open) {
		return null;
	}

	const [currentIndex, setCurrentIndex] = useState(point);

	const handleLeftButtonClick = () => {
		if (currentIndex > 0) {
			setCurrentIndex(currentIndex - 1);
		}
	};

	const handleRightButtonClick = () => {
		if (currentIndex < populationData.length - 1) {
			setCurrentIndex(currentIndex + 1);
		}
	};

	console.log(populationData[currentIndex]);

	const currentPop = populationData[currentIndex];
	const imgHeight = currentPop.img_height;

	// console.log(imgHeight, imgWidth);

	// console.log(currentIndex);

	const groupedDataPoints: any = {};
	Object.entries(currentPop.grid).forEach(([key, values]: any) => {
		if (!groupedDataPoints[key]) {
			groupedDataPoints[key] = [];
		}

		console.log(values);

		values.forEach((v: any) => {
			const [x, y] = v as [number, number];
			const flippedY = imgHeight - y;
			groupedDataPoints[key].push({ x, y: flippedY });
		});
	});

	// console.log(groupedDataPoints);

	const chartData = {
		datasets: Object.keys(groupedDataPoints).map((group) => ({
			label: `Group ${group}`,
			data: groupedDataPoints[group],
			backgroundColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${
				Math.random() * 255
			}, 0.7)`,
		})),
	};

	const formatTime = (timestampString: any) => {
		const dateTime = new Date(timestampString);
		return dateTime.toString();
	};

	const options = {
		// options: {
		// 	responsive: true,
		// 	maintainAspectRatio: false,
		// 	height: imgHeight,
		// 	width: 100,
		// },
		plugins: {
			legend: {
				display: false,
			},
		},
		scales: {
			x: {
				type: "linear",
				beginAtZero: true,
				// display: false,
			},
			y: {
				type: "linear",
				beginAtZero: true,
				// dispay: false,
			},
		},
		maintainAspectRatio: false,
	};

	return (
		<div className="c-modal-container">
			<div>
				<button className="c-close-button" onClick={onClose}>
					<img className="c-close-icon" src={CloseButton} alt="close" />
				</button>

				<div className="c-graph-container">
					<img
						src={backgroundImage}
						alt="background"
						style={{
							position: "absolute",
							top: "20px",
							left: "350px",
							width: "calc(50% - 150px)",
							height: "auto",
							opacity: 0.4,
						}}
					/>
					<div
						style={{
							position: "absolute",
							top: "20px",
							left: "310px",
							width: "calc(50% - 100px)",
							height: "340px",
							zIndex: 2,
						}}
					>
						<Scatter data={chartData} options={options} />
					</div>
				</div>
			</div>
			<div className="layout">
				<div>
					<button
						className="left"
						onClick={handleLeftButtonClick}
						disabled={currentIndex === 0}
					>
						Left
					</button>
					<div className="time">Time: {formatTime(currentPop.timestamp)}</div>
				</div>
				<div className="buttons-container">
					<button
						onClick={handleRightButtonClick}
						disabled={currentIndex === populationData.length - 1}
					>
						Right
					</button>
				</div>
			</div>
		</div>
	);
};

export default ClusterModal;
