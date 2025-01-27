import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";

const GroupedResults = ({ results, selectedOption }) => {
  if (results.length === 0 || selectedOption === "") {
    return (
      <Typography variant="h6" align="center">
        Results will appear here
      </Typography>
    );
  }
  results = JSON.parse(results);
  let columns = [];

  const paginationModel = { page: 0, pageSize: 5 };

  let rows = [];

  //   Adjust the rows/columns based on the selected option

  if (selectedOption === "member_name") {
    rows = results.map((result, index) => ({
      id: index,
      member_name: result.member_name,
      Keyword: result.Keyword,
      Tf_idf_value: result.Tf_idf_value,
    }));

    columns = [
      { field: "id", headerName: "ID", width: 200 },
      { field: "member_name", headerName: "Name", width: 200 },
      { field: "Keyword", headerName: "Keyword", width: 200 },
      { field: "Tf_idf_value", headerName: "Tf_idf_value", width: 150 },
    ];
  } else if (selectedOption === "date") {
    rows = results.map((result, index) => ({
      id: index,
      sitting_date: result.sitting_date,
      Keyword: result.Keyword,
      Tf_idf_value: result.Tf_idf_value,
    }));

    columns = [
      { field: "id", headerName: "ID", width: 200 },
      { field: "sitting_date", headerName: "Date", width: 200 },
      { field: "Keyword", headerName: "Keyword", width: 200 },
      { field: "Tf_idf_value", headerName: "Tf_idf_value", width: 150 },
    ];
  } else if (selectedOption === "party") {
    rows = results.map((result, index) => ({
      id: index,
      political_party: result.political_party,
      Keyword: result.Keyword,
      Tf_idf_value: result.Tf_idf_value,
    }));

    columns = [
      { field: "id", headerName: "ID", width: 200 },
      { field: "political_party", headerName: "Political Party", width: 200 },
      { field: "Keyword", headerName: "Keyword", width: 200 },
      { field: "Tf_idf_value", headerName: "Tf_idf_value", width: 150 },
    ];
  } else if (selectedOption === "speech") {
    rows = results.map((result, index) => ({
      id: index,
      speech: result.speech,
      Keyword: result.Keyword,
      Tf_idf_value: result.Tf_idf_value,
    }));

    columns = [
      { field: "id", headerName: "ID", width: 200 },
      { field: "speech", headerName: "Speech", width: 200 },
      { field: "Keyword", headerName: "Keyword", width: 200 },
      { field: "Tf_idf_value", headerName: "Tf_idf_value", width: 150 },
    ];
  }

  return (
    <Paper sx={{ height: 400, width: "35%" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{ border: 0 }}
      />
    </Paper>
  );
};

export default GroupedResults;
