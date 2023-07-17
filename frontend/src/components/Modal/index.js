import React from "react";

import "./index.css";

let positionData = {};

const Modal = ({ open, onClose, position }) => {
	if (!open) return null;

	// request to backend api to get positionData given position (lat/long)

	return (
		<div className="modal-container">
			<p>
				Modal Position | Latitude: {position.lat} | Longitude: {position.lng}
			</p>
			<button onClick={() => onClose()}>Close</button>
		</div>
	);
};

export default Modal;
