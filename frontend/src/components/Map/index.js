import React, { useMemo, useState } from "react";
import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";

import "./index.css";
import Modal from "../Modal";

const markerPositions = [
	{ lat: 43.47234048997899, lng: -80.54611173191944 },
	{ lat: 43.47215263406454, lng: -80.54390222557805 },
];

const Map = () => {
	const [openModal, setOpenModal] = useState(false);
	const [position, setPositionModal] = useState();

	const { isLoaded } = useLoadScript({
		googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
	});

	// add geocoding (address -> lat/long)
	const center = useMemo(
		() => ({ lat: 43.47234048997899, lng: -80.54611173191944 }),
		[]
	);

	if (!isLoaded) return <div>Loading...</div>;

	return (
		<div>
			<GoogleMap
				zoom={18}
				center={center}
				mapContainerClassName="map-container"
			>
				{markerPositions.map((pos) => (
					<MarkerF
						position={pos}
						onClick={() => {
							setPositionModal(pos);
							setOpenModal(true);
						}}
					/>
				))}
			</GoogleMap>
			<Modal
				open={openModal}
				onClose={() => setOpenModal(false)}
				position={position}
			/>
		</div>
	);
};

export default Map;
