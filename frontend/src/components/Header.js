// src/components/Header.js
import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

const Header = () => (
  <AppBar position="static">
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
        Greek Parliament Speech Search
      </Typography>
    </Toolbar>
  </AppBar>
);

export default Header;
