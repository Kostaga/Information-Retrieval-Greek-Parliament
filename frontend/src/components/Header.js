// src/components/Header.js
import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";
import { Link } from "react-router-dom";

const Header = () => (
  <AppBar position="static">
    <Toolbar>
      <Typography variant="h6" component="div">
        Greek Parliament Speech Search Engine
      </Typography>
      <Typography
        variant="h6"
        component="div"
        style={{ marginLeft: "1rem", marginRight: "1rem" }}
      >
        |
      </Typography>
      <Link
        to="/"
        style={{
          color: "inherit",
          textDecoration: "none",
          marginLeft: "2rem",
        }}
      >
        <Typography variant="h6" component="div">
          Home
        </Typography>
      </Link>
      <Link
        to="/group-speech"
        style={{ color: "inherit", textDecoration: "none", marginLeft: "2rem" }}
      >
        <Typography variant="h6" component="div">
          Group Speech
        </Typography>
      </Link>
    </Toolbar>
  </AppBar>
);

export default Header;
