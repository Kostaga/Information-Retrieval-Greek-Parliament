// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./Pages/Homepage";
import Group from "./Pages/Group";
import Clustering from "./Pages/Clustering";
import Footer from "./components/Footer";
import Header from "./components/Header";
import ParticlesBg from "particles-bg";
import "./App.css";

const App = () => {
  return (
    <Router>
      <ParticlesBg
        className="particles"
        color="#ffffff"
        num={80}
        type="cobweb"
        bg={true}
      />
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/group-speech" element={<Group />} />
        <Route path="/clustering" element={<Clustering />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
