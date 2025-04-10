import React from 'react';
import { useQuery } from 'react-query';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function Dashboard() {
  const { data: alertStats, isLoading: alertStatsLoading } = useQuery(
    'alertStats',
    async () => {
      const response = await axios.get(`${API_URL}/alerts/statistics`);
      return response.data;
    }
  );

  const { data: threats, isLoading: threatsLoading } = useQuery(
    'recentThreats',
    async () => {
      const response = await axios.get(`${API_URL}/threats?limit=10`);
      return response.data;
    }
  );

  if (alertStatsLoading || threatsLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  const alertData = {
    labels: ['New', 'Acknowledged', 'Resolved'],
    datasets: [
      {
        label: 'Alerts by Status',
        data: [
          alertStats?.by_status?.new || 0,
          alertStats?.by_status?.acknowledged || 0,
          alertStats?.by_status?.resolved || 0,
        ],
        backgroundColor: ['#ff6384', '#36a2eb', '#4bc0c0'],
      },
    ],
  };

  const threatData = {
    labels: threats?.map((threat) => 
      new Date(threat.timestamp).toLocaleDateString()
    ) || [],
    datasets: [
      {
        label: 'Threat Severity',
        data: threats?.map((threat) => threat.severity) || [],
        borderColor: '#4bc0c0',
        tension: 0.1,
      },
    ],
  };

  return (
    <Grid container spacing={3}>
      {/* Summary Cards */}
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Total Alerts
            </Typography>
            <Typography variant="h3">
              {alertStats?.total || 0}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Active Threats
            </Typography>
            <Typography variant="h3">
              {threats?.length || 0}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Alert Response Rate
            </Typography>
            <Typography variant="h3">
              {alertStats?.total ? 
                Math.round((alertStats.by_status.resolved / alertStats.total) * 100) : 0}%
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      {/* Charts */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Alert Distribution
          </Typography>
          <Box sx={{ height: 300 }}>
            <Bar
              data={alertData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
              }}
            />
          </Box>
        </Paper>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Threat Severity Trend
          </Typography>
          <Box sx={{ height: 300 }}>
            <Line
              data={threatData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
              }}
            />
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default Dashboard;
