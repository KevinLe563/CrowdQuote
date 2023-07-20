import React, { useMemo, useState } from "react";
import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";
import usePlacesAutocomplete, {
	getGeocode,
	getLatLng,
} from "use-places-autocomplete";
import {
	Combobox,
	ComboboxInput,
	ComboboxList,
	ComboboxOption,
	ComboboxPopover,
} from "@reach/combobox";

import "./index.css";
import Modal from "../Modal";

const markerPositions = [
	{ lat: 43.4723337, lng: -80.5461394, address: "address" },
	{ lat: 43.4721517, lng: -80.5439318, address: "address" },
	{ lat: 43.4745663, lng: -80.5327111, address: "address" },
];

const Map = () => {
	const [openModal, setOpenModal] = useState(false);
	const [position, setPositionModal] = useState(null);
	const [selected, setSelected] = useState(null);

	const { isLoaded } = useLoadScript({
		googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
		libraries: ["places"],
	});

	// geocoding (address -> lat/long)

	const center = useMemo(
		() =>
			selected ? selected : { lat: 43.47234048997899, lng: -80.54611173191944 },
		[selected]
	);

	if (!isLoaded) return <div>Loading...</div>;

	// reverse geocode to display address when hover
	// const reverseGeocode = () => {
	// 	const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`;
	// 	fetch(url).then((response) =>
	// 		response.json().then((location) => {
	// 			console.log(location);
	// 			//console.log(location.results[0].formatted_address);
	// 			return location.results[0].formatted_address;
	// 		})
	// 	);
	// };

	// for (var i = 0; i < 3; i++) {
	// 	console.log(markerPositions[i]["lat"], markerPositions[i]["lng"]);
	// 	markerPositions[i]["address"] = reverseGeocode();
	// }

	return (
		<div>
			<div className="search-container">
				<PlacesAutocomplete setSelected={setSelected} />
			</div>
			<div className="map-container">
				<GoogleMap zoom={18} center={center} mapContainerClassName="map">
					{markerPositions.map((pos) => (
						<MarkerF
							position={pos}
							title={pos["address"]}
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
		</div>
	);
};

const PlacesAutocomplete = ({ setSelected }) => {
	const {
		ready,
		value,
		setValue,
		suggestions: { status, data },
		clearSuggestions,
	} = usePlacesAutocomplete();

	const handleSelect = async (address) => {
		setValue(address, false);
		clearSuggestions();

		// convert address to geocode
		const results = await getGeocode({ address });
		const { lat, lng } = await getLatLng(results[0]);
		// console.log({ lat, lng });
		setSelected({ lat, lng });
	};

	return (
		<Combobox onSelect={handleSelect}>
			<ComboboxInput
				className="combobox-input"
				value={value}
				onChange={(e) => setValue(e.target.value)}
				disabled={!ready}
				placeholder="Search an address"
			></ComboboxInput>
			<ComboboxPopover>
				<ComboboxList>
					{status === "OK" &&
						data.map(({ place_id, description }) => (
							<ComboboxOption
								className="combobox-option"
								key={place_id}
								value={description}
							/>
						))}
				</ComboboxList>
			</ComboboxPopover>
		</Combobox>
	);
};

export default Map;
