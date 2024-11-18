import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";

const SearchBar = () => {
  // State to handle individual fields
  const [searchFields, setSearchFields] = useState({
    name: "",
    date: "",
    politicalParty: "",
    keywords: "",
  });

  // Handle input changes
  const handleChange = (field) => (event) => {
    setSearchFields({
      ...searchFields,
      [field]: event.target.value,
    });
  };

  // Handle the search action
  const handleSearch = () => {
    onSearch(searchFields);
  };

  // Function to handle search
  const onSearch = (searchFields) => {
    console.log("Search Fields: ", searchFields);
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh", // Full screen height
        flexDirection: "column",

        color: "#ffffff",
        padding: 3,
      }}
    >
      <Typography variant="h4" sx={{ marginBottom: 3 }}>
        Search Parliament Speeches by:
      </Typography>

      <p style={{ marginBottom: "2rem" }}>
        Leave empty for all speeches in a desired column
      </p>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          width: "100%",
          maxWidth: "600px",
        }}
      >
        {/* Input for Member Name */}
        <TextField
          label="Name of Member"
          value={searchFields.name}
          onChange={handleChange("name")}
          variant="outlined"
          fullWidth
          InputProps={{ style: { fontSize: "1rem" } }}
          InputLabelProps={{ style: { fontSize: "1rem", color: "#e6e6e6" } }}
          sx={{
            input: { color: "#ededed" },
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

        {/* Input for Date */}
        <TextField
          label="Date"
          value={searchFields.date}
          onChange={handleChange("date")}
          variant="outlined"
          fullWidth
          InputProps={{ style: { fontSize: "1rem" } }}
          InputLabelProps={{ style: { fontSize: "1rem", color: "#e6e6e6" } }}
          sx={{
            input: { color: "#ededed" },
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

        {/* Input for Political Party */}
        <TextField
          label="Political Party"
          value={searchFields.politicalParty}
          onChange={handleChange("politicalParty")}
          variant="outlined"
          fullWidth
          InputProps={{ style: { fontSize: "1rem" } }}
          InputLabelProps={{ style: { fontSize: "1rem", color: "#e6e6e6" } }}
          sx={{
            input: { color: "#ededed" },
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

        {/* Input for Keywords */}
        <TextField
          label="Keywords"
          value={searchFields.keywords}
          onChange={handleChange("keywords")}
          variant="outlined"
          fullWidth
          InputProps={{ style: { fontSize: "1rem" } }}
          InputLabelProps={{ style: { fontSize: "1rem", color: "#e6e6e6" } }}
          sx={{
            input: { color: "#ededed" },
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

        {/* Search Button */}
        <Button
          variant="contained"
          onClick={handleSearch}
          sx={{
            fontSize: "1.2rem",
            padding: 1,
            backgroundColor: "#388ceb",
            "&:hover": { backgroundColor: "#1e66c1" },
            borderRadius: 5,
          }}
        >
          Search
        </Button>
      </Box>
    </Box>
  );
};

export default SearchBar;
