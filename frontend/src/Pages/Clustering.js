import React, {useEffect, useState} from "react";
import { Typography, Box } from "@mui/material";

// const Clustering = () => {
//   const [plotPath, setPlotPath] = useState("");

//   useEffect(() => {
//     fetch("http://localhost:5000/clustering", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         setPlotPath(`http://localhost:5000/${data.plot_path}`);  // Ensure it matches backend
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//       });
//   }, []);
const Clustering = () => {
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    setImageUrl("http://127.0.0.1:5000/clustering"); // Flask endpoint
  }, []);
  
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

      {/* Plot Image
      {plotPath && <img src={plotPath} alt="Cluster Plot" />} */}
      {imageUrl ? (
        <img src={imageUrl} alt="Speech Clustering Plot" style={{ width: "80%", border: "2px solid black" }} />
      ) : (
        <p>Loading...</p>
      )}
    </Box>
  );
};

export default Clustering;