import React from "react";
import { Typography, Box } from "@mui/material";

const Clustering = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        padding: 2,
      }}
    >
      {/* Title */}
      <Typography
        variant="h3"
        sx={{
          marginBottom: 3,
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        K-Means Clustering of Speeches
      </Typography>

      {/* Plot Image */}
      <img src="http://localhost:5000/static/kmeans_plot.png" alt="K-Means Clustering Plot" />
    </Box>
  );
};

export default Clustering;