import React from "react";
import { Box, Typography } from "@mui/material";

const Footer = () => (
  <Box
    sx={{
      backgroundColor: "white",
      padding: "5px 20px",
      position: "relative",
      bottom: 0,
      width: "100%",
      textAlign: "center",
      boxShadow: "0 -2px 5px rgba(0,0,0,0.1)",
      marginTop: "auto", // Ensure footer stays at the bottom of the page
    }}
  >
    <Typography variant="body2" color="textSecondary" padding={0.5}>
      © 2024-25 Konstantinos Agathopoulos 4119 | Dimitra Angelidou 4200
    </Typography>
    <Typography variant="body2" color="textSecondary">
      Information Retrieval Project
    </Typography>
  </Box>
);

export default Footer;
