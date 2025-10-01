# 🌾 Smart Agriculture Crop Planner

A farmer-friendly web application built with **Streamlit** that helps farmers choose the **best crops** to grow based on soil type, rainfall, and location. The app predicts **pest risk**, recommends fertilizers, visualizes crop data, and supports **6 Indian regional languages**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 Description

This application empowers farmers, especially those with minimal literacy or technical knowledge, to make **data-driven decisions** about crop selection. With a simple, intuitive interface featuring **dropdowns, sliders, and visual charts**, farmers can:

- Select their farm parameters (soil type, rainfall, location)
- Get personalized crop recommendations
- View profit estimates and yield predictions
- Understand pest risks and fertilizer needs
- Track historical searches
- Export reports for record-keeping

---

## ✨ Key Features

### 🌍 Multi-Language Support
- **6 Indian Languages**: English, Kannada (ಕನ್ನಡ), Tamil (தமிழ்), Telugu (తెలుగు), Malayalam (മലയാളം), Hindi (हिंदी)
- All UI elements, labels, and instructions dynamically translate

### 🧑‍🌾 Farmer-Friendly Interface
- **No typing required** - uses dropdowns and sliders only
- Large buttons and clear visual indicators
- Color-coded risk levels (🟢 Low, 🟡 Medium, 🔴 High)
- Simple 3-step process: Select → Recommend → Export

### 📊 Smart Recommendations
- **Intelligent filtering** based on soil type, rainfall (200-3000mm), and state
- **Profit optimization** - crops sorted by highest profit potential
- **Yield predictions** per hectare
- **Pest risk analysis** with mitigation suggestions
- **Fertilizer recommendations** (NPK, Urea, DAP, Potash, Organic)
- **Market price insights** for better decision-making

### 📈 Data Visualizations
- **Profit comparison charts** (Bar charts)
- **Yield analysis** (Interactive graphs)
- **Market price trends** (Visual comparisons)
- **Pest risk distribution** (Pie charts)
- **Crop cycle information** (Duration and seasons)

### 💾 Data Management
- **SQLite database** for efficient data storage
- **Search history tracking** - view past recommendations
- **CSV export** - download crop reports for offline use
- **Expandable crop database** - easy to add new crops

### 🔒 Additional Features
- No hardcoded secrets - environment-friendly
- Error handling to prevent crashes
- Responsive design for mobile/tablet access
- Sample data included for immediate testing

---

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Step-by-Step Installation

#### 1️⃣ Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/yourusername/smart-agriculture-crop-planner.git
cd smart-agriculture-crop-planner
```

**Option B: Manual Download**
- Download the ZIP file from GitHub
- Extract to a folder
- Open terminal/command prompt in that folder

---

#### 2️⃣ Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `plotly` - Interactive charts
- `sqlite3-python` - Database support
- `openpyxl` - Excel export support

---

#### 4️⃣ Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy the URL from the terminal and paste it into your browser.

---

#### 5️⃣ Using the App

1. **Select Language** - Choose from the sidebar (English, Kannada, Tamil, Telugu, Malayalam, Hindi)
2. **Choose Soil Type** - Select from 6 soil types (Clay, Sandy, Loamy, Black, Red, Alluvial)
3. **Set Rainfall** - Use the slider to set average annual rainfall (200-3000mm)
4. **Select Location** - Choose your state from the dropdown
5. **Enter Farm Size** - Input your farm size in hectares
6. **Get Recommendations** - Click the button to see crop suggestions
7. **View Results** - Explore profit estimates, charts, and pest risk info
8. **Export Report** - Download CSV for offline reference

---

## 📦 Project Structure

```
smart-agriculture-crop-planner/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── agriculture.db         # SQLite database (auto-generated)
├── .gitignore            # Git ignore file
│
└── screenshots/          # App screenshots (optional)
```

---

## 🗃️ Database Schema

### Crops Table
```sql
CREATE TABLE crops (
    id INTEGER PRIMARY KEY,
    name_en TEXT, name_kn TEXT, name_ta TEXT, 
    name_te TEXT, name_ml TEXT, name_hi TEXT,
    soil_types TEXT,
    min_rainfall INTEGER,
    max_rainfall INTEGER,
    states TEXT,
    yield_per_hectare REAL,
    profit_per_hectare INTEGER,
    pest_risk TEXT,
    fertilizer TEXT,
    market_price REAL,
    season TEXT,
    water_requirement TEXT,
    duration_months INTEGER
);
```

### Search History Table
```sql
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    soil_type TEXT,
    rainfall INTEGER,
    location TEXT,
    farm_size REAL,
    recommended_crops TEXT
);
```

---

## 🧪 Sample Test Inputs

### Test Case 1: Rice Farmer in Karnataka
- **Soil Type**: Loamy Soil / ಲೋಮಿ ಮಣ್ಣು
- **Rainfall**: 1500mm
- **Location**: Karnataka / ಕರ್ನಾಟಕ
- **Farm Size**: 2 hectares
- **Expected Results**: Rice, Banana, Sugarcane

### Test Case 2: Wheat Farmer in Punjab
- **Soil Type**: Alluvial Soil / ਜਲੋਢ ਮਿੱਟੀ
- **Rainfall**: 600mm
- **Location**: Punjab / ਪੰਜਾਬ
- **Farm Size**: 5 hectares
- **Expected Results**: Wheat, Maize

### Test Case 3: Cotton Farmer in Maharashtra
- **Soil Type**: Black Soil / काली मिट्टी
- **Rainfall**: 800mm
- **Location**: Maharashtra / महाराष्ट्र
- **Farm Size**: 3 hectares
- **Expected Results**: Cotton, Sugarcane, Onion

### Test Case 4: Vegetable Farmer in Tamil Nadu
- **Soil Type**: Red Soil / சிவப்பு மண்
- **Rainfall**: 900mm
- **Location**: Tamil Nadu / தமிழ்நாடு
- **Farm Size**: 1 hectare
- **Expected Results**: Tomato, Chilli, Groundnut

---

## 🔧 Troubleshooting

### Problem: "Module not found" error
**Solution**: Make sure you've activated the virtual environment and installed requirements
```bash
pip install -r requirements.txt
```

### Problem: Port 8501 already in use
**Solution**: Kill the existing process or use a different port
```bash
streamlit run app.py --server.port 8502
```

### Problem: Database errors
**Solution**: Delete `agriculture.db` and restart the app (it will auto-regenerate)
```bash
rm agriculture.db  # On macOS/Linux
del agriculture.db  # On Windows
```

### Problem: Streamlit not opening in browser
**Solution**: Manually open the URL shown in terminal
```
http://localhost:8501
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web framework for UI |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive visualizations |
| **SQLite** | Lightweight database |
| **CSS** | Custom styling |

---

## 📱 Mobile Compatibility

The app is **fully responsive** and works on:
- 📱 Mobile phones (Android/iOS)
- 📱 Tablets (iPad, Android tablets)
- 💻 Desktop computers
- 🖥️ Laptops

---

## 🌟 Future Enhancements

- [ ] Weather API integration for real-time data
- [ ] SMS notifications for crop alerts
- [ ] Voice input support for illiterate farmers
- [ ] Government scheme recommendations
- [ ] Nearby market price tracking
- [ ] Crop disease image detection (AI/ML)
- [ ] Water requirement calculator
- [ ] Soil testing recommendations
- [ ] Community forum for farmers
- [ ] Offline mode support

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - Initial work - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Crop data sourced from agricultural research papers
- Icons from [Flaticon](https://www.flaticon.com/)
- Inspiration from real farmer needs
- Built with ❤️ for Indian farmers

---

## 📞 Support

For support, email: support@yourapp.com  
Or create an issue on [GitHub Issues](https://github.com/yourusername/smart-agriculture-crop-planner/issues)

---

## 📸 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Crop Recommendations
![Recommendations](screenshots/recommendations.png)

### Data Visualizations
![Charts](screenshots/charts.png)

---

## 🌐 Live Demo

Try the live demo: [Smart Agriculture Crop Planner](https://your-demo-link.com)

---

## ⭐ Star this repo if you find it helpful!

**Made with 🌾 for farmers, by developers**