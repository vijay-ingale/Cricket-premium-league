# 🏏 Rating System - Quick Reference Card

## 📏 Performance Benchmarks

### **Batsman:**
- Excellent Runs: **60+**
- Excellent SR: **200+**
- Excellent Sixes: **6+**
- Excellent Fours: **8+**

### **Bowler:**
- Excellent Wickets: **4+**
- Excellent Economy: **6.0 or lower**
- Excellent Overs: **4.0+**

---

## 📊 Rating Formulas

### **Batsman (0-5 scale)**
```
Each metric scored against benchmark (capped at 1.0):
- Runs Score = min(Runs / 60, 1.0)
- SR Score = min(SR / 200, 1.0)
- Sixes Score = min(Sixes / 6, 1.0)
- Fours Score = min(Fours / 8, 1.0)

Rating = (Runs×30% + SR×25% + Sixes×30% + Fours×15%) × 5
```

**Example:** 79 runs, 161 SR, 7 sixes, 4 fours
```
Runs: min(79/60, 1.0) = 1.0
SR: min(161/200, 1.0) = 0.806
Sixes: min(7/6, 1.0) = 1.0
Fours: min(4/8, 1.0) = 0.5

Rating = (1.0×0.30 + 0.806×0.25 + 1.0×0.30 + 0.5×0.15) × 5
       = 4.4 ⭐ (rounds to 4 🟢)
```

### **Bowler (0-5 scale)**
```
Each metric scored against benchmark:
- Wickets Score = min(Wickets / 4, 1.0)
- Economy Score = min(6.0 / Economy, 1.0)  [inverted]
- Overs Score = min(Overs / 4.0, 1.0)

Rating = (Wickets×50% + Economy×30% + Overs×20%) × 5
```

**Example:** 3 wickets, 7.5 economy, 4 overs
```
Wickets: min(3/4, 1.0) = 0.75
Economy: min(6.0/7.5, 1.0) = 0.80
Overs: min(4.0/4.0, 1.0) = 1.0

Rating = (0.75×0.50 + 0.80×0.30 + 1.0×0.20) × 5
       = 4.1 ⭐ (rounds to 4 🟢)
```

### **All-rounder (0-5 scale)**
```
Rating = Batting×40% + Bowling×40% + MVP×20%
```

---

## ✅ Key Advantage: Fair & Independent

**Each player rated on their OWN performance:**
- ✅ Not affected by others' exceptional/poor performance
- ✅ Consistent across different matches
- ✅ 79 runs always gets similar rating, regardless of match
- ✅ Fair to all players

---

## 🔄 Cumulative Rating

**Formula:** Weighted average (recent matches weighted higher)

**Example:**
```
Match 1 (old): 2.5 × weight 0.25 = 0.625
Match 2:       3.0 × weight 0.33 = 0.990
Match 3:       3.5 × weight 0.50 = 1.750
Match 4 (new): 4.2 × weight 1.00 = 4.200
                                   -------
Total: 7.565 / 2.08 = 3.6 (rounded to 4)
```

---

## 🎯 Which Rating is Used?

| Rating | Used for Teams? |
|--------|----------------|
| New (this match) | ❌ No |
| Cumulative (calculated) | ❌ No |
| **Current (in database)** | ✅ **YES!** |

---

## 🎨 Rating Colors

- ⚪ **0** - Not Rated
- 🔴 **1** - Very Low
- 🟠 **2** - Low
- 🟡 **3** - Medium
- 🟢 **4** - High
- 🔵 **5** - Excellent

---

## 📝 Quick Workflow

1. **Upload PDFs** → System calculates ratings
2. **Map names** → Match PDF names to database
3. **Review & Edit** → Adjust if needed
4. **Apply** → Updates current rating
5. **Generate Teams** → Uses current ratings

---

## 💡 Pro Tips

✅ **Recent matches matter more** in cumulative calculation
✅ **Manual override** available anytime
✅ **Current rating** = what's used for teams
✅ **Rating history** shows all past matches
✅ **Auto button** reverts to calculated rating

---

**Need more details?** See RATING_SYSTEM_GUIDE.md
