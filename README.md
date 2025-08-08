![image](https://github.com/user-attachments/assets/0160ef99-32fc-4547-a0e5-f678f3a660a1)

# COVID-19 Data AI Project

## What It Is
An AI-powered dashboard that:
- Visualizes Toronto COVID-19 cases on an interactive map
- Shows detailed case information by neighbourhood
- Uses machine learning for case similarity analysis

## What It Does
1. Geocodes Toronto neighbourhoods from raw data
2. Stores COVID cases in MongoDB Atlas database
3. Displays cases on a live-updating map
4. Shows case details when clicking neighbourhoods
5. Generates AI embeddings for semantic analysis

## Done So Far ✅
- MongoDB setup with COVID cases and geocoded neighbourhoods
- Automated pipeline for geocoding neighbourhood coordinates
- Interactive dashboard with:
  - Case clusters on map (size = case count)
  - Detailed case table (updates on click)
- AI model initialized for embeddings
- Production server setup (Waitress)

## What's Left 🔜
1. **AI Features**
   - Store embeddings in MongoDB
   - Implement similarity search
   - Add "find similar cases" functionality

2. **Dashboard Improvements**
   - Date range filters
   - Demographic charts (age/gender)
   - Case outcome statistics
   - Source of infection analysis

3. **Deployment**
   - Docker containerization
   - Cloud deployment (AWS/Azure)
   - User authentication

## Progress
- Data Pipeline: [██████████] 100%
- Core Dashboard: [████████░░] 80%
- AI Integration: [███░░░░░░░] 30%
- Deployment Ready: [██░░░░░░░░] 20%
