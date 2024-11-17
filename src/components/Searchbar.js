import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (onSearch) onSearch(query);
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh", // Full screen height
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          alignItems: "center",
          width: "100%",
          maxWidth: "600px",
        }}
      >
        <TextField
          label="Search Speeches"
          inputProps={{ style: { fontSize: "1.5rem" } }}
          InputLabelProps={{ style: { fontSize: "1.5rem" } }}
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          fullWidth
          sx={{
            color: "white",
            "& .MuiInputLabel-root": {
              color: "#e6e6e6", // Label color for contrast
            },
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: "#ffffff", // Border color
              },
              "&:hover fieldset": {
                borderColor: "#ffffff", // Border color on hover
              },
              "&.Mui-focused fieldset": {
                borderColor: "#ffffff", // Border color when focused
              },
            },
          }}
        />
        <Button
          variant="contained"
          onClick={handleSearch}
          disabled={!query.trim()}
          sx={{
            color: "white",
            fontSize: "1.2rem",
            width: "100%",
            backgroundColor: "#388ceb",
          }}
        >
          Search
        </Button>
      </Box>
    </Box>
  );
};

export default SearchBar;
