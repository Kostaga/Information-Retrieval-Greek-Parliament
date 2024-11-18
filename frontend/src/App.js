// src/App.js
import React from "react";
import HomePage from "./Pages/Homepage";
import Footer from "./components/Footer";
import Header from "./components/Header";
import ParticlesBg from "particles-bg";
import "./App.css";

const App = () => {
  return (
    <>
      <ParticlesBg
        className="particles"
        color="#ffffff"
        num={80}
        type="cobweb"
        bg={true}
      />
      <Header />
      <HomePage />
      <Footer />
    </>
  );
};

export default App;
