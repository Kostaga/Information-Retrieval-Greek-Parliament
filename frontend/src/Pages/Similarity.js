import React, { useState } from "react";
import { Typography, Box, CircularProgress, Paper, TextField, Button } from "@mui/material";

const Similarity = () => {
  const [similarities, setSimilarities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [k, setK] = useState(""); // Start empty to wait for user input
  const [error, setError] = useState("");

  const fetchSimilarities = () => {
    if (!k || k <= 0) {
      setError("Please enter a valid positive number.");
      return;
    }
    setError("");
    setLoading(true);

    fetch(`http://localhost:5000/similarity?k=${k}`)
      .then((response) => response.json())
      .then((data) => {
        setSimilarities(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching similarity data:", error);
        setLoading(false);
      });
  };

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
      <Typography variant="h3" sx={{ marginBottom: 3, fontWeight: "bold", textAlign: "center" }}>
        Similarity between Parliament Members
      </Typography>

      {/* Input for K */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 2, marginBottom: 3 }}>
        <TextField
          type="number"
          label="Enter Top K pairs"
          value={k}
          onChange={(e) => setK(e.target.value)}
          inputProps={{ min: 1 }}
          sx={{
            "& .MuiInputBase-input": {
              color: "white", // Make text inside the input white
            },
            "& .MuiInputLabel-root": {
              color: "white", // Make label (placeholder) white
            },
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: "white", // Make the border white
              },
              "&:hover fieldset": {
                borderColor: "white", // Keep border white on hover
              },
              "&.Mui-focused fieldset": {
                borderColor: "white", // Keep border white when focused
              },
            },
          }}
        />
        <Button variant="contained" onClick={fetchSimilarities}>
          Fetch
        </Button>
      </Box>

      {/* Show error if invalid input */}
      {error && <Typography color="error">{error}</Typography>}

      {/* Loading Indicator */}
      {loading ? (
        <CircularProgress />
      ) : similarities.length > 0 ? (
        <Box sx={{ width: "100%", maxWidth: 600 }}>
          {similarities.map((pair, index) => (
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
          ))}
        </Box>
      ) : (
        !loading &&
        !error &&
        similarities.length === 0 && (
          <Typography variant="body1">No results. Please enter a number and fetch data.</Typography>
        )
      )}
    </Box>
  );
};

export default Similarity;
