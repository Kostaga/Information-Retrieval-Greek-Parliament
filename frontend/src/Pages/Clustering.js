import React, {useEffect, useState} from "react";
import { Typography, Box, CircularProgress } from "@mui/material";

const Clustering = () => {
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/clustering")
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setImageUrl(url);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching clustering image:", error);
        setLoading(false);
      });
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

      {/* Plot Image */}
      {loading ? (
        <CircularProgress />
      ) : (
        imageUrl && (
          <img
            src={imageUrl}
            alt="Speech Clustering Plot"
            style={{ width: "60%", border: "2px solid black" }}
          />
        )
      )}
    </Box>
  );
};

export default Clustering;