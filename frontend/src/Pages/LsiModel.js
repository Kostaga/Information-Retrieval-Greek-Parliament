import React, { useEffect, useState } from "react";
import { Typography, Box, CircularProgress, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TablePagination } from "@mui/material";

const LsiModel = () => {
  const [lsiVectors, setLsiVectors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    // Fetch LSI vectors from Flask API
    fetch("http://localhost:5000/lsi")
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched data:", data); // Log the fetched data
        setLsiVectors(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching LSI vectors:", error);
        setLoading(false);
      });
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
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
        LSI Vectorization of Speeches
      </Typography>

      {/* Loading Indicator */}
      {loading ? (
        <CircularProgress />
      ) : (
        <Box sx={{ width: "100%", maxWidth: 800 }}>
          {lsiVectors.length > 0 ? (
            <Paper>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Speech Index</TableCell>
                      <TableCell>LSI Vector</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {lsiVectors.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((vector, index) => (
                      <TableRow key={index}>
                        <TableCell>{index + 1 + page * rowsPerPage}</TableCell>
                        <TableCell>
                          {vector.map(([topic, weight]) => (
                            <div key={topic}>
                              Topic {topic}: {weight.toFixed(4)}
                            </div>
                          ))}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={lsiVectors.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </Paper>
          ) : (
            <Typography variant="body1" color="error">
              No LSI data available.
            </Typography>
          )}
        </Box>
      )}
    </Box>
  );
};

export default LsiModel;