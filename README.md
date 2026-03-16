# 🏏 Cricket Team Builder

A simple and beautiful application to create balanced cricket teams for your weekend matches.

## Features
- ✅ Store players permanently in database
- ✅ Select players for each match
- ✅ Auto-generate balanced teams
- ✅ Manual team adjustments
- ✅ Beautiful, modern UI

## Running with Docker

### First Time Setup
```cmd
docker-compose up -d
```

### Access the App
Open your browser to: `http://localhost:8501`

### Data Persistence
Your player data is stored in the `./data/players_data.json` file on your local machine.

**Important:** If you rebuild the container, your data is safe in the `data` folder!

### Stop the App
```cmd
docker-compose down
```

### Rebuild After Code Changes
```cmd
docker-compose down
docker-compose up --build -d
```

## Running Locally (Without Docker)

### Install Dependencies
```cmd
pip install -r requirements.txt
```

### Run the App
```cmd
streamlit run app.py
```

## Usage

1. **Add Players** (First Time)
   - Use sidebar to add all your players to the database
   - Categorize them as Batsman, Bowler, or All-rounder

2. **Select Players** (Every Weekend)
   - Use tabs to view each category
   - Check boxes for available players
   - Use "Select All" or "Deselect All" buttons

3. **Create Teams**
   - Choose number of teams
   - Click "Generate Teams"
   - Teams will be balanced automatically

4. **Adjust Teams** (Optional)
   - Move players between teams manually
   - Edit team names
   - Reshuffle if needed

## Troubleshooting

### Players Not Showing After Rebuild
If you rebuilt the Docker container and lost your players:
1. Check if `data/players_data.json` exists on your machine
2. If it doesn't exist, you need to add players again
3. The file will be created automatically when you add the first player

### Docker Desktop Not Running
Make sure Docker Desktop is running before using `docker-compose` commands.
