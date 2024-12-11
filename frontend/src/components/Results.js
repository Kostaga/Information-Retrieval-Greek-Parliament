import React from "react";
import { Paper, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { Box, height } from "@mui/system";

const Results = ({ results }) => {
  if (results.length === 0) {
    return (
      <Typography variant="h6" align="center">
        Results will appear here
      </Typography>
    );
  }

  const columns = [
    { field: "id", headerName: "ID", width: 200 },
    { field: "member_name", headerName: "Name", width: 200 },
    { field: "sitting_date", headerName: "Date", width: 200 },
    { field: "political_party", headerName: "Political Party", width: 200 },
    {
      field: "speech",
      headerName: "Speech",
      flex: 1,
    },
  ];

  const rows = results.map((result, index) => ({
    id: index,
    member_name: result.member_name,
    sitting_date: result.sitting_date,
    political_party: result.political_party,
    speech: result.speech,
  }));

  return (
    <Paper
      sx={{
        height: 500,
        width: "60%",
        color: "white",
        marginBottom: "5rem",
        marginTop: "2rem",
        padding: "1rem",
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{ border: 0 }}
        autosizeOnMount
      />
    </Paper>
  );
};

export default Results;
