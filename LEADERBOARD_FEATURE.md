# 🏆 Latest Match Leaderboard Feature

## 📊 Overview

The leaderboard dashboard displays the top 5 performers from the most recent match in three categories:
- 🏏 Top 5 Batsmen
- ⚡ Top 5 Bowlers
- ⭐ Top 5 MVP

---

## 🎯 How It Works

### **Step 1: Upload Match Reports**
When you upload batting, bowling, and MVP PDFs:
1. System parses all player data
2. Saves it as "latest leaderboard"
3. Stores in `data/latest_leaderboard.json`

### **Step 2: View Leaderboard**
In Rating Manager, scroll to "🏆 Latest Match Leaderboard" section to see:
- Match date
- Top 5 in each category
- Key stats for each player

### **Step 3: Upload New Reports**
When you upload new PDFs:
- Old leaderboard is **overwritten**
- New leaderboard becomes the "latest"
- Previous data is replaced

---

## 📋 Leaderboard Display

### **Top 5 Batsmen (sorted by Runs)**
```
🥇 Shaifesh
   89 runs | SR: 296.67 | 6s: 12 | 4s: 3

🥈 Shivchandra Bhosle
   79 runs | SR: 161.22 | 6s: 7 | 4s: 4

🥉 Suraj Gunjal
   77 runs | SR: 220.00 | 6s: 10 | 4s: 2

4. Bhalchandra Pawar
   75 runs | SR: 241.94 | 6s: 11 | 4s: 0

5. Dhiraj Jadhav
   64 runs | SR: 206.45 | 6s: 8 | 4s: 1
```

### **Top 5 Bowlers (sorted by Wickets)**
```
🥇 Player A
   4 wickets | Econ: 6.5 | Overs: 4.0

🥈 Player B
   3 wickets | Econ: 7.0 | Overs: 3.5

🥉 Player C
   3 wickets | Econ: 7.5 | Overs: 4.0
```

### **Top 5 MVP (sorted by Total Points)**
```
🥇 Player X
   Total: 95 | Bat: 50 | Bowl: 45

🥈 Player Y
   Total: 88 | Bat: 60 | Bowl: 28

🥉 Player Z
   Total: 82 | Bat: 45 | Bowl: 37
```

---

## 💾 Data Storage

### **File Location:**
`data/latest_leaderboard.json`

### **File Structure:**
```json
{
  "date": "2026-01-30",
  "batting": [
    {
      "Player Name": "Shaifesh",
      "Runs": 89,
      "SR": 296.67,
      "4s": 3,
      "6s": 12
    },
    ...
  ],
  "bowling": [
    {
      "Player Name": "Player A",
      "Wickets": 4,
      "Econ": 6.5,
      "Overs": 4.0
    },
    ...
  ],
  "mvp": [
    {
      "Player Name": "Player X",
      "Total": 95,
      "Batting": 50,
      "Bowling": 45
    },
    ...
  ]
}
```

---

## 🔄 Update Behavior

### **When You Upload New Reports:**

**Before:**
```
Latest Leaderboard: Jan 25, 2026
- Top batsman: Player A (75 runs)
```

**After Uploading Jan 30 Reports:**
```
Latest Leaderboard: Jan 30, 2026
- Top batsman: Shaifesh (89 runs)
```

**Result:** Jan 25 data is **replaced** by Jan 30 data

---

## 🎨 Visual Design

### **Layout:**
- Three columns side-by-side
- Color-coded borders:
  - 🏏 Batsmen: Teal (#14b8a6)
  - ⚡ Bowlers: Blue (#3b82f6)
  - ⭐ MVP: Orange (#f59e0b)

### **Medals:**
- 🥇 1st place
- 🥈 2nd place
- 🥉 3rd place
- 4. / 5. for 4th and 5th

---

## 💡 Use Cases

### **1. Post-Match Recognition**
- Quickly see who performed best
- Share top performers with team
- Celebrate achievements

### **2. Performance Tracking**
- Compare with previous matches
- Identify consistent performers
- Spot emerging talent

### **3. Team Selection**
- See current form
- Make informed decisions
- Balance teams based on recent performance

---

## 🔧 Customization

### **Change Number of Players Shown:**
Edit `app.py`, find:
```python
batting_sorted = sorted(batting_data, key=lambda x: x.get('Runs', 0), reverse=True)[:5]
```
Change `[:5]` to `[:10]` for top 10

### **Change Sorting Criteria:**

**Batsmen by Strike Rate instead of Runs:**
```python
batting_sorted = sorted(batting_data, key=lambda x: x.get('SR', 0), reverse=True)[:5]
```

**Bowlers by Economy instead of Wickets:**
```python
bowling_sorted = sorted(bowling_data, key=lambda x: x.get('Econ', 999), reverse=False)[:5]
```

---

## 📊 Integration with Rating System

The leaderboard is **independent** from the rating system:

| Feature | Leaderboard | Rating System |
|---------|-------------|---------------|
| **Data Source** | Latest match only | All match history |
| **Purpose** | Show top performers | Calculate player ratings |
| **Updates** | Overwritten each match | Cumulative history |
| **Display** | Top 5 lists | Individual ratings |

---

## 🎯 Key Points

✅ **Shows latest match only** - Not historical
✅ **Automatically updated** - When new PDFs uploaded
✅ **Top 5 in each category** - Batsmen, Bowlers, MVP
✅ **Persistent storage** - Survives app restart
✅ **Visual & clear** - Easy to read at a glance

---

## 📞 Questions?

**Q: Can I see previous match leaderboards?**
A: No, only the latest is stored. Consider saving screenshots if needed.

**Q: What if I upload PDFs out of order?**
A: The most recent upload becomes "latest", regardless of match date.

**Q: Can I manually edit the leaderboard?**
A: No, it's automatically generated from PDFs. Edit the PDF data if needed.

---

**Last Updated:** January 30, 2026
**Version:** 1.0
