import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  IconButton,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  Check as CheckIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Threats() {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedThreat, setSelectedThreat] = useState(null);

  const { data: threats, isLoading } = useQuery(
    ['threats', page, rowsPerPage],
    async () => {
      const response = await axios.get(
        `${API_URL}/threats?skip=${page * rowsPerPage}&limit=${rowsPerPage}`
      );
      return response.data;
    }
  );

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewThreat = (threat) => {
    setSelectedThreat(threat);
  };

  const handleCloseThreat = () => {
    setSelectedThreat(null);
  };

  const getSeverityColor = (severity) => {
    if (severity >= 0.8) return 'error';
    if (severity >= 0.5) return 'warning';
    return 'success';
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Threat Detection
      </Typography>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Source IP</TableCell>
                <TableCell>Destination IP</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {threats?.map((threat) => (
                <TableRow key={threat.id}>
                  <TableCell>{threat.id}</TableCell>
                  <TableCell>{threat.threat_type}</TableCell>
                  <TableCell>
                    <Chip
                      label={`${Math.round(threat.severity * 100)}%`}
                      color={getSeverityColor(threat.severity)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{threat.source_ip}</TableCell>
                  <TableCell>{threat.destination_ip}</TableCell>
                  <TableCell>
                    <Chip
                      label={threat.status}
                      color={
                        threat.status === 'resolved'
                          ? 'success'
                          : threat.status === 'analyzing'
                          ? 'warning'
                          : 'error'
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(threat.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleViewThreat(threat)}
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={-1}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25]}
        />
      </Paper>

      {/* Threat Details Dialog */}
      <Dialog open={!!selectedThreat} onClose={handleCloseThreat} maxWidth="md" fullWidth>
        <DialogTitle>Threat Details</DialogTitle>
        <DialogContent>
          {selectedThreat && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {selectedThreat.threat_type}
              </Typography>
              <Typography variant="body1" paragraph>
                Severity: {Math.round(selectedThreat.severity * 100)}%
              </Typography>
              <Typography variant="body1" paragraph>
                Source IP: {selectedThreat.source_ip}
              </Typography>
              <Typography variant="body1" paragraph>
                Destination IP: {selectedThreat.destination_ip}
              </Typography>
              <Typography variant="body1" paragraph>
                Status: {selectedThreat.status}
              </Typography>
              <Typography variant="body1" paragraph>
                Timestamp: {new Date(selectedThreat.timestamp).toLocaleString()}
              </Typography>
              <Typography variant="body1" paragraph>
                Raw Data:
              </Typography>
              <pre>
                {JSON.stringify(selectedThreat.raw_data, null, 2)}
              </pre>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseThreat}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Threats;
