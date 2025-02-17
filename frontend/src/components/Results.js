import {
  Paper,
  Typography,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
} from "@mui/material";
import React, { useState } from "react";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const Results = ({ results }) => {
  const [expandedRows, setExpandedRows] = useState({});
  const [page, setPage] = useState(0);
  const [rowsPerPage] = useState(5);

  const handleExpandClick = (id) => {
    setExpandedRows((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

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
      width: 200,
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
    <div style={{ padding: "1rem" }}>
      <TableContainer
        component={Paper}
        style={{
          width: "100%",
          maxHeight: "40vh",
          overflow: "scroll",
          padding: "1rem",
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell key={column.field}>{column.headerName}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row) => (
                <React.Fragment key={row.id}>
                  <TableRow>
                    {columns.map((column) => (
                      <TableCell key={column.field}>
                        {column.field === "speech" ? (
                          <>
                            <IconButton
                              onClick={() => handleExpandClick(row.id)}
                              aria-expanded={expandedRows[row.id]}
                              aria-label="show more"
                            >
                              <ExpandMoreIcon />
                            </IconButton>
                            {expandedRows[row.id]
                              ? row[column.field]
                              : row[column.field].substring(0, 100) + "..."}
                          </>
                        ) : (
                          row[column.field]
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                </React.Fragment>
              ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[5]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
        />
      </TableContainer>
    </div>
  );
};

export default Results;
