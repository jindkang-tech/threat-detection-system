import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
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
  TextField,
  CircularProgress,
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  Check as CheckIcon,
  Comment as CommentIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Alerts() {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [commentDialog, setCommentDialog] = useState(false);
  const [comment, setComment] = useState('');
  const queryClient = useQueryClient();

  const { data: alerts, isLoading } = useQuery(
    ['alerts', page, rowsPerPage],
    async () => {
      const response = await axios.get(
        `${API_URL}/alerts?skip=${page * rowsPerPage}&limit=${rowsPerPage}`
      );
      return response.data;
    }
  );

  const updateAlertStatus = useMutation(
    async ({ alertId, status }) => {
      const response = await axios.put(
        `${API_URL}/alerts/${alertId}/status?status=${status}`
      );
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('alerts');
      },
    }
  );

  const addComment = useMutation(
    async ({ alertId, text }) => {
      const response = await axios.post(
        `${API_URL}/alerts/${alertId}/comment`,
        { text }
      );
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('alerts');
        handleCloseComment();
      },
    }
  );

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewAlert = (alert) => {
    setSelectedAlert(alert);
  };

  const handleCloseAlert = () => {
    setSelectedAlert(null);
  };

  const handleOpenComment = (alert) => {
    setSelectedAlert(alert);
    setCommentDialog(true);
  };

  const handleCloseComment = () => {
    setCommentDialog(false);
    setComment('');
  };

  const handleSubmitComment = () => {
    if (comment.trim() && selectedAlert) {
      addComment.mutate({
        alertId: selectedAlert.id,
        text: comment,
      });
    }
  };

  const handleAcknowledge = (alertId) => {
    updateAlertStatus.mutate({ alertId, status: 'acknowledged' });
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
        Alert Management
      </Typography>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Message</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {alerts?.map((alert) => (
                <TableRow key={alert.id}>
                  <TableCell>{alert.id}</TableCell>
                  <TableCell>{alert.alert_type}</TableCell>
                  <TableCell>{alert.message}</TableCell>
                  <TableCell>
                    <Chip
                      label={alert.status}
                      color={
                        alert.status === 'resolved'
                          ? 'success'
                          : alert.status === 'acknowledged'
                          ? 'warning'
                          : 'error'
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(alert.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleViewAlert(alert)}
                    >
                      <VisibilityIcon />
                    </IconButton>
                    {alert.status === 'new' && (
                      <IconButton
                        size="small"
                        onClick={() => handleAcknowledge(alert.id)}
                      >
                        <CheckIcon />
                      </IconButton>
                    )}
                    <IconButton
                      size="small"
                      onClick={() => handleOpenComment(alert)}
                    >
                      <CommentIcon />
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

      {/* Alert Details Dialog */}
      <Dialog open={!!selectedAlert && !commentDialog} onClose={handleCloseAlert} maxWidth="md" fullWidth>
        <DialogTitle>Alert Details</DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {selectedAlert.alert_type}
              </Typography>
              <Typography variant="body1" paragraph>
                Message: {selectedAlert.message}
              </Typography>
              <Typography variant="body1" paragraph>
                Status: {selectedAlert.status}
              </Typography>
              <Typography variant="body1" paragraph>
                Timestamp: {new Date(selectedAlert.timestamp).toLocaleString()}
              </Typography>
              <Typography variant="body1" paragraph>
                Metadata:
              </Typography>
              <pre>
                {JSON.stringify(selectedAlert.metadata, null, 2)}
              </pre>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAlert}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Comment Dialog */}
      <Dialog open={commentDialog} onClose={handleCloseComment}>
        <DialogTitle>Add Comment</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Comment"
            fullWidth
            multiline
            rows={4}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseComment}>Cancel</Button>
          <Button onClick={handleSubmitComment} variant="contained" color="primary">
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Alerts;
