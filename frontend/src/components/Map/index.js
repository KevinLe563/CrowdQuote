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
	{ lat: 43.4723337, lng: -80.5461394 },
	{ lat: 43.4721517, lng: -80.5439318 },
	{ lat: 43.4745663, lng: -80.5327111 },
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

	return (
		<div>
			<div className="search-container">
				<PlacesAutocomplete setSelected={setSelected} />
			</div>
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
					{status == "OK" &&
						data.map(({ place_id, description }) => (
							<ComboboxOption key={place_id} value={description} />
						))}
				</ComboboxList>
			</ComboboxPopover>
		</Combobox>
	);
};

export default Map;
