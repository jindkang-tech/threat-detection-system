import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  LinearProgress,
  Alert,
  TextField,
} from '@mui/material';
import {
  Timeline,
  PlayArrow as TrainIcon,
  Save as SaveIcon,
  Upload as LoadIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Models() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [trainingData, setTrainingData] = useState(null);
  const queryClient = useQueryClient();

  const { data: models, isLoading } = useQuery('models', async () => {
    const response = await axios.get(`${API_URL}/models`);
    return response.data;
  });

  const trainModel = useMutation(
    async ({ modelName, data }) => {
      const response = await axios.post(
        `${API_URL}/models/${modelName}/train`,
        data
      );
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('models');
        handleCloseDialog();
      },
    }
  );

  const handleOpenDialog = (model) => {
    setSelectedModel(model);
  };

  const handleCloseDialog = () => {
    setSelectedModel(null);
    setTrainingData(null);
  };

  const handleTrainModel = () => {
    if (selectedModel && trainingData) {
      trainModel.mutate({
        modelName: selectedModel,
        data: JSON.parse(trainingData),
      });
    }
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
        ML Models Management
      </Typography>

      <Grid container spacing={3}>
        {Object.entries(models || {}).map(([name, info]) => (
          <Grid item xs={12} md={6} lg={4} key={name}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {name}
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Type: {info.model_type}
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Last Training: {info.last_training_time || 'Never'}
                </Typography>
                {info.accuracy && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="body2" color="textSecondary" sx={{ mr: 1 }}>
                      Accuracy:
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={info.accuracy * 100}
                      sx={{ flexGrow: 1 }}
                    />
                    <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                      {Math.round(info.accuracy * 100)}%
                    </Typography>
                  </Box>
                )}
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<TrainIcon />}
                  onClick={() => handleOpenDialog(name)}
                >
                  Train
                </Button>
                <Button size="small" startIcon={<SaveIcon />}>
                  Save
                </Button>
                <Button size="small" startIcon={<LoadIcon />}>
                  Load
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Training Dialog */}
      <Dialog open={!!selectedModel} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>Train Model: {selectedModel}</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            Provide training data in JSON format. Include features and labels arrays.
          </Alert>
          <TextField
            fullWidth
            multiline
            rows={10}
            label="Training Data (JSON)"
            value={trainingData || ''}
            onChange={(e) => setTrainingData(e.target.value)}
            error={trainingData && !isValidJSON(trainingData)}
            helperText={
              trainingData && !isValidJSON(trainingData)
                ? 'Invalid JSON format'
                : ''
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleTrainModel}
            variant="contained"
            color="primary"
            disabled={!trainingData || !isValidJSON(trainingData)}
          >
            Train Model
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

function isValidJSON(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}

export default Models;
