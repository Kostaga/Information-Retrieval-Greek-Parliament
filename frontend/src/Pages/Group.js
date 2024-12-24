import React, { useState } from "react";
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Box,
} from "@mui/material";
import GroupedResults from "../components/GroupedResults";

const GroupSpeeches = () => {
  const [selectedOption, setSelectedOption] = useState("");
  const [groupedResults, setGroupedResults] = useState([]);

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);

    // Send the selected option to the backend
    fetch("http://localhost:5000/groupedData", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ grouped_by: event.target.value }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Set the results to the data received
        console.log(data);

        setGroupedResults(data);
      })

      .catch((error) => {
        console.error("Error:", error);
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
      {/* Title */}
      <Typography
        variant="h3"
        sx={{
          marginBottom: 3,
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        Group Speeches
      </Typography>

      {/* Select Field */}
      <FormControl
        fullWidth
        sx={{
          maxWidth: 400, // Limits width for better alignment
          marginBottom: 3,
        }}
      >
        <InputLabel
          id="group-by-label"
          sx={{
            color: "#fff", // Default label color
            "&.Mui-focused": {
              color: "#fff", // Label color when focused
            },
          }}
        >
          Group By
        </InputLabel>
        <Select
          labelId="group-by-label"
          value={selectedOption}
          label="Group By"
          onChange={handleSelectChange}
          sx={{
            color: "#fff", // Selected text color
            border: "1px solid #fff", // Border color
            "& .MuiOutlinedInput-notchedOutline": {
              borderColor: "#fff", // Default border color
            },
            "&:hover .MuiOutlinedInput-notchedOutline": {
              borderColor: "#fff", // Hover border color
            },
            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
              borderColor: "#fff", // Focused border color
            },
            "& .MuiSvgIcon-root": {
              color: "#fff", // Dropdown arrow color
            },
          }}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value="member_name">Member Name</MenuItem>
          <MenuItem value="date">Date</MenuItem>
          <MenuItem value="party">Political Party</MenuItem>
          <MenuItem value="speech">Speech</MenuItem>
        </Select>
      </FormControl>

      {/* Display Selected Option */}
      {selectedOption && (
        <Typography
          variant="h6"
          sx={{
            marginTop: 2,
            textAlign: "center",
          }}
        >
          Selected Group By: {selectedOption}
        </Typography>
      )}

      {/* Display Grouped Results */}
      {groupedResults.length > 0 && (
        <Typography
          variant="h6"
          sx={{
            marginTop: 2,
            textAlign: "center",
          }}
        ></Typography>
      )}

      <GroupedResults
        results={groupedResults}
        selectedOption={selectedOption}
      />
    </Box>
  );
};

export default GroupSpeeches;
