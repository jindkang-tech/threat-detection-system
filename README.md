# AI-Driven Threat Detection System

An advanced threat detection system leveraging AI/ML for real-time threat detection, automated incident response, and intelligent alert management.

## Features

- Real-time threat detection using ML/AI
- Automated incident response
- Intelligent alert system
- SIEM integration
- Analyst dashboard
- GDPR compliant data handling

## Tech Stack

- **Backend**: FastAPI (Python)
- **Machine Learning**: TensorFlow, PyTorch, Scikit-learn
- **NLP**: NLTK, spaCy, Hugging Face Transformers
- **Databases**: 
  - PostgreSQL (structured data)
  - MongoDB (unstructured data)
- **SIEM Integration**: IBM QRadar, Wazuh
- **Frontend**: React

## Project Structure

```
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── ml/           # ML models
│   │   └── utils/        # Utility functions
├── frontend/             # React frontend
├── ml_models/            # ML model training
├── tests/                # Test suite
└── docker/               # Docker configuration
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jindkang-tech/threat-detection-system.git
cd threat-detection-system
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm start
```

## Development

### Mock Data Integration
The system currently uses mock data services for development and testing. This allows for:
- Rapid development without requiring actual threat data
- Testing of various scenarios and edge cases
- Development of UI components with realistic data

### API Endpoints

#### Alerts
- `GET /alerts` - List all alerts
- `GET /alerts/{alert_id}` - Get specific alert details
- `GET /alerts/statistics` - Get alert statistics
- `PUT /alerts/{alert_id}/status` - Update alert status

#### Threats
- `GET /threats` - List detected threats
- `GET /threats/{threat_id}` - Get specific threat details

#### Models
- `GET /models` - List available ML models
- `GET /models/{model_id}` - Get specific model details

### Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

### End-to-End Testing
E2E tests can be run using Cypress:
```bash
cd frontend
npm run e2e
```

## Security & Compliance

This system is designed with security and compliance in mind:
- GDPR compliant data handling
- Secure API endpoints
- Data encryption
- Regular security audits

## Deployment

### Docker Deployment
The project includes Docker configuration for easy deployment:

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop all services
docker-compose down
```

### Environment Variables
Copy the example environment files and update them with your settings:
```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

### Production Deployment
1. Update environment variables for production
2. Build frontend for production: `cd frontend && npm run build`
3. Use a production-grade WSGI server for the backend
4. Set up SSL/TLS certificates
5. Configure reverse proxy (e.g., Nginx)



### Quality Gates
- All tests must pass
- Code coverage requirements
- Security scan results
- Performance benchmarks
