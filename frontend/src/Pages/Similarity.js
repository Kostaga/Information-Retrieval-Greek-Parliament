import React, { useEffect, useState } from "react";
import { Typography, Box, CircularProgress, Paper } from "@mui/material";

const Similarity = () => {
  const [similarities, setSimilarities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch similarity data from Flask API
    fetch("http://localhost:5000/similarity")
      .then((response) => response.json())
      .then((data) => {
        setSimilarities(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching similarity data:", error);
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
        Similarity between Parliament Members
      </Typography>

      {/* Loading Indicator */}
      {loading ? (
        <CircularProgress />
      ) : (
        <Box sx={{ width: "100%", maxWidth: 600 }}>
          {similarities.length > 0 ? (
            similarities.map((pair, index) => (
              <Paper
                key={index}
                sx={{
                  padding: 2,
                  marginBottom: 2,
                  textAlign: "center",
                  backgroundColor: "#f5f5f5",
                }}
              >
                <Typography variant="h5">
                  {pair.member_1} & <span style={{ fontWeight: "bold" }}>{pair.member_2}</span>
                </Typography>
                <Typography variant="body1">
                  Similarity Score: <strong>{pair.score}</strong>

                </Typography>
              </Paper>
            ))
          ) : (
            <Typography variant="body1" color="error">
              No similarity data available.
            </Typography>
          )}
        </Box>
      )}
    </Box>
  );
};

export default Similarity;
