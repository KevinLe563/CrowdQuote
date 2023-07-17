import React from "react";

import "./index.css";
import Header from "../Header";
import Map from "../Map";
import Footer from "../Footer";

const Home = () => {
	return (
		<div className="home-container">
			<Header />
			<Map />
			<Footer />
		</div>
	);
};

export default Home;
