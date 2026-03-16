# 🏏 Cricket Team Builder - Rating System Guide

## 📊 Overview

The rating system automatically calculates player ratings (0-5 scale) based on **individual match performance** against fixed benchmarks. Each player is rated on their own performance, NOT by comparing with others in the match.

---

## 🎯 How Ratings Work

### **Rating Scale:**
- ⚪ **0** - Not Rated / No data
- 🔴 **1** - Very Low (0-20% of excellent)
- 🟠 **2** - Low (20-40% of excellent)
- 🟡 **3** - Medium (40-60% of excellent)
- 🟢 **4** - High (60-80% of excellent)
- 🔵 **5** - Excellent (80-100%+ of excellent)

---

## 📏 Performance Benchmarks

### **Batsman Benchmarks:**
- **Excellent Runs:** 60+ runs
- **Excellent Strike Rate:** 200+
- **Excellent Sixes:** 6+
- **Excellent Fours:** 8+

### **Bowler Benchmarks:**
- **Excellent Wickets:** 4+
- **Excellent Economy:** 6.0 or lower
- **Excellent Overs:** 4.0+

### **All-rounder:**
- Combination of batting + bowling + MVP score

---

## 📈 Rating Calculation Examples

### **Example 1: Batsman - Vijay Ingale**

**Match Performance:**
- Runs: 89
- Strike Rate: 296.67
- Fours: 3
- Sixes: 12

**How Rating is Calculated (Against Benchmarks):**

1. **Runs Score:**
   ```
   Score = min(89 / 60, 1.0) = min(1.48, 1.0) = 1.0
   (Exceeded excellent benchmark!)
   ```

2. **Strike Rate Score:**
   ```
   Score = min(296.67 / 200, 1.0) = min(1.48, 1.0) = 1.0
   (Exceeded excellent benchmark!)
   ```

3. **Sixes Score:**
   ```
   Score = min(12 / 6, 1.0) = min(2.0, 1.0) = 1.0
   (Doubled the excellent benchmark!)
   ```

4. **Fours Score:**
   ```
   Score = min(3 / 8, 1.0) = 0.375
   (37.5% of excellent benchmark)
   ```

5. **Apply Weights:**
   ```
   Rating = (Runs×30% + SR×25% + Sixes×30% + Fours×15%) × 5
   Rating = (1.0×0.30 + 1.0×0.25 + 1.0×0.30 + 0.375×0.15) × 5
   Rating = (0.30 + 0.25 + 0.30 + 0.056) × 5
   Rating = 0.906 × 5
   Rating = 4.5
   ```

**Result:** Vijay gets **4.5** rating ⭐ (rounds to **5** 🔵)

---

### **Example 2: Batsman - Shivchandra Bhosle**

**Match Performance:**
- Runs: 79
- Strike Rate: 161.22
- Fours: 4
- Sixes: 7

**How Rating is Calculated (Against Benchmarks):**

1. **Runs Score:**
   ```
   Score = min(79 / 60, 1.0) = min(1.32, 1.0) = 1.0
   (Exceeded excellent benchmark!)
   ```

2. **Strike Rate Score:**
   ```
   Score = min(161.22 / 200, 1.0) = 0.806
   (80.6% of excellent benchmark)
   ```

3. **Sixes Score:**
   ```
   Score = min(7 / 6, 1.0) = min(1.17, 1.0) = 1.0
   (Exceeded excellent benchmark!)
   ```

4. **Fours Score:**
   ```
   Score = min(4 / 8, 1.0) = 0.5
   (50% of excellent benchmark)
   ```

5. **Apply Weights:**
   ```
   Rating = (1.0×0.30 + 0.806×0.25 + 1.0×0.30 + 0.5×0.15) × 5
   Rating = (0.30 + 0.202 + 0.30 + 0.075) × 5
   Rating = 0.877 × 5
   Rating = 4.4
   ```

**Result:** Shivchandra gets **4.4** rating ⭐ (rounds to **4** 🟢)

---

### **Example 3: Bowler - Balaji**

**Match Performance:**
- Wickets: 3
- Economy: 7.5
- Overs: 4.0

**How Rating is Calculated (Against Benchmarks):**

1. **Wickets Score:**
   ```
   Score = min(3 / 4, 1.0) = 0.75
   (75% of excellent benchmark)
   ```

2. **Economy Score (lower is better):**
   ```
   Score = min(6.0 / 7.5, 1.0) = 0.80
   (Economy is 80% as good as excellent)
   ```

3. **Overs Score:**
   ```
   Score = min(4.0 / 4.0, 1.0) = 1.0
   (Met excellent benchmark!)
   ```

4. **Apply Weights:**
   ```
   Rating = (Wickets×50% + Economy×30% + Overs×20%) × 5
   Rating = (0.75×0.50 + 0.80×0.30 + 1.0×0.20) × 5
   Rating = (0.375 + 0.24 + 0.20) × 5
   Rating = 0.815 × 5
   Rating = 4.1
   ```

**Result:** Balaji gets **4.1** rating ⭐ (rounds to **4** 🟢)

---

## 🔄 Cumulative Rating Explained

### **What is Cumulative Rating?**

Cumulative rating is a **weighted average** of all match ratings, where **recent matches matter more**.

### **Example: Bala's Rating History**

**Match History:**
1. **Jan 15, 2026:** Rating = 2.5 (oldest)
2. **Jan 20, 2026:** Rating = 3.0
3. **Jan 25, 2026:** Rating = 3.5
4. **Jan 30, 2026:** Rating = 4.2 (newest)

**How Cumulative is Calculated:**

```
Weight for match 1 (oldest): 1/4 = 0.25
Weight for match 2: 1/3 = 0.33
Weight for match 3: 1/2 = 0.50
Weight for match 4 (newest): 1/1 = 1.00

Cumulative = (2.5×0.25 + 3.0×0.33 + 3.5×0.50 + 4.2×1.00) / (0.25+0.33+0.50+1.00)
Cumulative = (0.625 + 0.99 + 1.75 + 4.20) / 2.08
Cumulative = 7.565 / 2.08
Cumulative = 3.6
```

**Result:** Bala's cumulative rating = **3.6** (rounded to **4** for team creation)

### **Why Weighted Average?**

✅ **Recent performance matters more** - A player improving gets higher rating
✅ **One bad match doesn't ruin rating** - Smoothed over time
✅ **Fair representation** - Considers all matches but emphasizes recent form

---

## 🎮 Which Rating is Used for Team Creation?

### **Answer: CURRENT RATING (from database)**

The "Current" rating in the database is what's used for team generation. This can be:

1. **Auto-calculated cumulative** (if you click "Apply" after uploading PDFs)
2. **Manually set** (if you override in Manual Rating Override section)

### **Rating Types Comparison:**

| Rating Type | What It Is | Where You See It | Used for Teams? |
|------------|------------|------------------|-----------------|
| **New** | This match only | After uploading PDF | ❌ No (preview only) |
| **Cumulative** | Weighted average of all matches | Rating Manager | ❌ No (calculation only) |
| **Current** | What's in database | Everywhere | ✅ **YES - This is used!** |

---

## 📝 Step-by-Step Workflow

### **Step 1: Upload Match PDFs**
- Upload batting, bowling, and MVP leaderboard PDFs
- System parses all player stats

### **Step 2: Map Player Names (if needed)**
- If PDF name differs from database (e.g., "Dhiraj" vs "Dhiraj Jadhav")
- Map PDF name to database player OR add as new player

### **Step 3: Review Calculated Ratings**
- System shows:
  - **Current:** Rating in database now
  - **New:** Rating from this match
  - **Edit box:** Adjust if needed
  - **Cumulative:** What it will become after applying

### **Step 4: Apply Ratings**
- Click "Apply" for individual player OR "Apply All"
- New rating added to history
- Cumulative recalculated
- Current rating updated to cumulative (rounded)

### **Step 5: Generate Teams**
- System automatically redirects to Team Builder
- Uses updated "Current" ratings
- Creates balanced teams using snake draft

---

## 🎯 Real Example: Complete Flow

### **Player: Nitin (Batsman)**

**Before Match:**
- Current Rating: 3
- Match History: 3 matches (ratings: 2.8, 3.0, 3.2)

**After Match (Jan 30):**
- Scored 79 runs, SR 161.22, 4 sixes
- **New Rating Calculated:** 3.8

**When You Click "Apply":**
1. Rating 3.8 added to history
2. Cumulative recalculated:
   ```
   (2.8×0.25 + 3.0×0.33 + 3.2×0.50 + 3.8×1.00) / 2.08 = 3.4
   ```
3. Current rating updated: 3 → **3** (rounded from 3.4)

**For Team Generation:**
- Nitin's rating = **3** (Current rating)
- Used to balance teams with other players

---

## ⚙️ Manual Override

### **When to Use:**
- Player is new (no match history)
- You disagree with automatic calculation
- Want to boost/reduce for team balance
- Testing different team combinations

### **How to Use:**
1. Go to Rating Manager
2. Scroll to "Manual Rating Override"
3. Find player
4. Change rating in edit box
5. Click "💾 Save"

**Note:** Manual override sets "Current" rating directly, ignoring cumulative calculation.

---

## 🔑 Key Takeaways

✅ **Ratings are 0-5 scale** based on match performance
✅ **Cumulative rating** = weighted average (recent matches matter more)
✅ **Current rating** = what's used for team generation
✅ **You can manually override** any rating anytime
✅ **System is flexible** - automatic calculation + manual control

---

## 📞 Questions?

If you have questions about:
- How a specific rating was calculated
- Why cumulative differs from current
- How to adjust ratings manually

Check the Rating Manager → Rating History section to see all past matches and ratings!

---

**Last Updated:** January 30, 2026
**Version:** 2.0
