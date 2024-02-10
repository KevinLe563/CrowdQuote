import React, { useState } from "react";
import { Scatter } from "react-chartjs-2";
import CloseButton from "../../assets/imgs/x.svg";
import "./index.css";

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

	const jsonString = populationData[currentIndex].grid;
	const jsonObject = JSON.parse(jsonString);

	console.log(currentIndex);

	const groupedDataPoints: any = {};
	Object.entries(jsonObject).forEach(([key, value]) => {
		if (!groupedDataPoints[key]) {
			groupedDataPoints[key] = [];
		}
		const coord: any = value[0];
		const [x, y] = coord as [number, number];
		groupedDataPoints[key].push({ x, y });
	});

	console.log(groupedDataPoints);

	const chartData = {
		datasets: Object.keys(groupedDataPoints).map((group) => ({
			label: `Group ${group}`,
			data: groupedDataPoints[group],
			backgroundColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${
				Math.random() * 255
			}, 0.7)`,
		})),
	};

	const options = {
		scales: {
			x: {
				type: "linear",
			},
			y: {
				type: "linear",
			},
		},
	};

	return (
		<div className="c-modal-container">
			<div style={{ backgroundImage: `url(/path/to/layout.jpg)` }}>
				<button className="c-close-button" onClick={onClose}>
					<img className="c-close-icon" src={CloseButton} alt="close" />
				</button>
				<div className="c-graph-container">
					<Scatter data={chartData} options={options} />
				</div>
			</div>
			<div className="buttons-container">
				<button onClick={handleLeftButtonClick} disabled={currentIndex === 0}>
					Left
				</button>
				<button
					onClick={handleRightButtonClick}
					disabled={currentIndex === populationData.length - 1}
				>
					Right
				</button>
			</div>
		</div>
	);
};

export default ClusterModal;
