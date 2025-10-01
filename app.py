import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
import os

# Page configuration
st.set_page_config(
    page_title="Smart Agriculture Crop Planner",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Translation dictionary
TRANSLATIONS = {
    'en': {
        'title': 'Smart Agriculture Crop Planner 🌾',
        'subtitle': 'Plan your crops smartly with data-driven insights',
        'select_language': 'Select Language',
        'soil_type': 'Soil Type',
        'rainfall': 'Average Annual Rainfall (mm)',
        'location': 'Farm Location (State)',
        'farm_size': 'Farm Size (hectares)',
        'get_suggestions': 'Get Crop Suggestions',
        'best_crops': 'Best Crops for Your Farm',
        'crop': 'Crop',
        'expected_yield': 'Expected Yield (tons/hectare)',
        'profit': 'Estimated Profit (₹/hectare)',
        'total_profit': 'Total Estimated Profit',
        'pest_risk': 'Pest Risk',
        'fertilizer': 'Recommended Fertilizer',
        'crop_cycle': 'Crop Cycle Calendar',
        'market_prices': 'Average Market Prices',
        'comparison': 'Crop Comparison',
        'price': 'Price (₹/kg)',
        'select_all': 'Please select all options',
        'no_crops': 'No suitable crops found',
        'adjust': 'Try adjusting your parameters',
        'about': 'About This App',
        'about_text': 'This application helps farmers make informed decisions about crop selection based on soil type, rainfall, and location.',
        'weather_info': 'Weather Information',
        'season': 'Best Season',
        'water_req': 'Water Requirement',
        'duration': 'Growing Duration',
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'export_report': 'Export Report',
        'history': 'Search History',
        'clay': 'Clay Soil',
        'sandy': 'Sandy Soil',
        'loamy': 'Loamy Soil',
        'black': 'Black Soil',
        'red': 'Red Soil',
        'alluvial': 'Alluvial Soil',
    },
    'kn': {
        'title': 'ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಬೆಳೆ ಯೋಜಕ 🌾',
        'subtitle': 'ಡೇಟಾ-ಆಧಾರಿತ ಒಳನೋಟಗಳೊಂದಿಗೆ ನಿಮ್ಮ ಬೆಳೆಗಳನ್ನು ಚತುರವಾಗಿ ಯೋಜಿಸಿ',
        'select_language': 'ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ',
        'soil_type': 'ಮಣ್ಣಿನ ಪ್ರಕಾರ',
        'rainfall': 'ಸರಾಸರಿ ವಾರ್ಷಿಕ ಮಳೆ (ಮಿಮೀ)',
        'location': 'ಜಮೀನು ಸ್ಥಳ (ರಾಜ್ಯ)',
        'farm_size': 'ಜಮೀನು ಗಾತ್ರ (ಹೆಕ್ಟೇರ್)',
        'get_suggestions': 'ಬೆಳೆ ಸಲಹೆಗಳನ್ನು ಪಡೆಯಿರಿ',
        'best_crops': 'ನಿಮ್ಮ ಜಮೀನಿಗೆ ಉತ್ತಮ ಬೆಳೆಗಳು',
        'crop': 'ಬೆಳೆ',
        'expected_yield': 'ನಿರೀಕ್ಷಿತ ಇಳುವರಿ (ಟನ್/ಹೆಕ್ಟೇರ್)',
        'profit': 'ಅಂದಾಜು ಲಾಭ (₹/ಹೆಕ್ಟೇರ್)',
        'total_profit': 'ಒಟ್ಟು ಅಂದಾಜು ಲಾಭ',
        'pest_risk': 'ಕೀಟ ಅಪಾಯ',
        'fertilizer': 'ಶಿಫಾರಸು ಮಾಡಿದ ರಸಗೊಬ್ಬರ',
        'crop_cycle': 'ಬೆಳೆ ಚಕ್ರ ಕ್ಯಾಲೆಂಡರ್',
        'market_prices': 'ಸರಾಸರಿ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು',
        'comparison': 'ಬೆಳೆ ಹೋಲಿಕೆ',
        'price': 'ಬೆಲೆ (₹/ಕೆಜಿ)',
        'select_all': 'ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಆಯ್ಕೆಗಳನ್ನು ಆರಿಸಿ',
        'no_crops': 'ಸೂಕ್ತ ಬೆಳೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ',
        'adjust': 'ನಿಮ್ಮ ಪ್ಯಾರಾಮೀಟರ್‌ಗಳನ್ನು ಸರಿಹೊಂದಿಸಲು ಪ್ರಯತ್ನಿಸಿ',
        'season': 'ಉತ್ತಮ ಋತು',
        'water_req': 'ನೀರಿನ ಅಗತ್ಯತೆ',
        'duration': 'ಬೆಳವಣಿಗೆಯ ಅವಧಿ',
        'low': 'ಕಡಿಮೆ',
        'medium': 'ಮಧ್ಯಮ',
        'high': 'ಹೆಚ್ಚು',
        'clay': 'ಜೇಡಿಮಣ್ಣು',
        'sandy': 'ಮರಳು ಮಣ್ಣು',
        'loamy': 'ಲೋಮಿ ಮಣ್ಣು',
        'black': 'ಕಪ್ಪು ಮಣ್ಣು',
        'red': 'ಕೆಂಪು ಮಣ್ಣು',
        'alluvial': 'ಮೆಕ್ಕಲು ಮಣ್ಣು',
    },
    'ta': {
        'title': 'ஸ்மார்ட் விவசாய பயிர் திட்டமிடுபவர் 🌾',
        'subtitle': 'தரவு அடிப்படையிலான நுண்ணறிவுகளுடன் உங்கள் பயிர்களை திட்டமிடுங்கள்',
        'select_language': 'மொழியை தேர்ந்தெடுக்கவும்',
        'soil_type': 'மண் வகை',
        'rainfall': 'சராசரி ஆண்டு மழை (மிமீ)',
        'location': 'பண்ணை இடம் (மாநிலம்)',
        'farm_size': 'பண்ணை அளவு (ஹெக்டேர்)',
        'get_suggestions': 'பயிர் பரிந்துரைகளைப் பெறுங்கள்',
        'best_crops': 'உங்கள் பண்ணைக்கு சிறந்த பயிர்கள்',
        'crop': 'பயிர்',
        'expected_yield': 'எதிர்பார்க்கப்படும் விளைச்சல் (டன்/ஹெக்டேர்)',
        'profit': 'மதிப்பிடப்பட்ட லாபம் (₹/ஹெக்டேர்)',
        'total_profit': 'மொத்த மதிப்பிடப்பட்ட லாபம்',
        'pest_risk': 'பூச்சி ஆபத்து',
        'fertilizer': 'பரிந்துரைக்கப்பட்ட உரம்',
        'crop_cycle': 'பயிர் சுழற்சி காலண்டர்',
        'market_prices': 'சராசரி சந்தை விலைகள்',
        'comparison': 'பயிர் ஒப்பீடு',
        'price': 'விலை (₹/கிலோ)',
        'select_all': 'தயவுசெய்து அனைத்து விருப்பங்களையும் தேர்ந்தெடுக்கவும்',
        'no_crops': 'பொருத்தமான பயிர்கள் இல்லை',
        'adjust': 'உங்கள் அளவுருக்களை சரிசெய்ய முயற்சிக்கவும்',
        'season': 'சிறந்த பருவம்',
        'water_req': 'நீர் தேவை',
        'duration': 'வளரும் காலம்',
        'low': 'குறைவு',
        'medium': 'நடுத்தர',
        'high': 'அதிகம்',
        'clay': 'களிமண்',
        'sandy': 'மணல் மண்',
        'loamy': 'கலப்பு மண்',
        'black': 'கருப்பு மண்',
        'red': 'சிவப்பு மண்',
        'alluvial': 'வண்டல் மண்',
    },
    'te': {
        'title': 'స్మార్ట్ వ్యవసాయ పంట ప్రణాళికాకర్త 🌾',
        'subtitle': 'డేటా-ఆధారిత అంతర్దృష్టులతో మీ పంటలను తెలివిగా ప్రణాళికాబద్ధం చేయండి',
        'select_language': 'భాషను ఎంచుకోండి',
        'soil_type': 'నేల రకం',
        'rainfall': 'సగటు వార్షిక వర్షపాతం (మిమీ)',
        'location': 'వ్యవసాయ స్థలం (రాష్ట్రం)',
        'farm_size': 'వ్యవసాయ పరిమాణం (హెక్టార్లు)',
        'get_suggestions': 'పంట సూచనలను పొందండి',
        'best_crops': 'మీ వ్యవసాయానికి ఉత్తమ పంటలు',
        'crop': 'పంట',
        'expected_yield': 'అంచనా దిగుబడి (టన్లు/హెక్టారు)',
        'profit': 'అంచనా లాభం (₹/హెక్టారు)',
        'total_profit': 'మొత్తం అంచనా లాభం',
        'pest_risk': 'తెగులు ప్రమాదం',
        'fertilizer': 'సిఫార్సు చేసిన ఎరువులు',
        'crop_cycle': 'పంట చక్రం క్యాలెండర్',
        'market_prices': 'సగటు మార్కెట్ ధరలు',
        'comparison': 'పంట పోలిక',
        'price': 'ధర (₹/కేజీ)',
        'select_all': 'దయచేసి అన్ని ఎంపికలను ఎంచుకోండి',
        'no_crops': 'తగిన పంటలు కనుగొనబడలేదు',
        'adjust': 'మీ పారామితులను సర్దుబాటు చేయడానికి ప్రయత్నించండి',
        'season': 'ఉత్తమ కాలం',
        'water_req': 'నీటి అవసరం',
        'duration': 'పెరుగుతున్న వ్యవధి',
        'low': 'తక్కువ',
        'medium': 'మధ్యస్థ',
        'high': 'ఎక్కువ',
        'clay': 'మట్టి నేల',
        'sandy': 'ఇసుక నేల',
        'loamy': 'లోమీ నేల',
        'black': 'నల్ల నేల',
        'red': 'ఎరుపు నేల',
        'alluvial': 'ఒండ్రు నేల',
    },
    'ml': {
        'title': 'സ്മാർട്ട് കാർഷിക വിള ആസൂത്രകൻ 🌾',
        'subtitle': 'ഡാറ്റ-അടിസ്ഥാന ഉൾക്കാഴ്ചകളോടെ നിങ്ങളുടെ വിളകൾ മികച്ച രീതിയിൽ ആസൂത്രണം ചെയ്യുക',
        'select_language': 'ഭാഷ തിരഞ്ഞെടുക്കുക',
        'soil_type': 'മണ്ണിന്റെ തരം',
        'rainfall': 'ശരാശരി വാർഷിക മഴ (മിമി)',
        'location': 'കൃഷിസ്ഥലം (സംസ്ഥാനം)',
        'farm_size': 'കൃഷിസ്ഥല വലുപ്പം (ഹെക്ടർ)',
        'get_suggestions': 'വിള നിർദ്ദേശങ്ങൾ നേടുക',
        'best_crops': 'നിങ്ങളുടെ കൃഷിസ്ഥലത്തിനുള്ള മികച്ച വിളകൾ',
        'crop': 'വിള',
        'expected_yield': 'പ്രതീക്ഷിക്കുന്ന വിളവ് (ടൺ/ഹെക്ടർ)',
        'profit': 'കണക്കാക്കിയ ലാഭം (₹/ഹെക്ടർ)',
        'total_profit': 'ആകെ കണക്കാക്കിയ ലാഭം',
        'pest_risk': 'കീടബാധ അപകടം',
        'fertilizer': 'ശുപാർശ ചെയ്ത വളം',
        'crop_cycle': 'വിള ചക്രം കലണ്ടർ',
        'market_prices': 'ശരാശരി വിപണി വിലകൾ',
        'comparison': 'വിള താരതമ്യം',
        'price': 'വില (₹/കിലോ)',
        'select_all': 'ദയവായി എല്ലാ ഓപ്ഷനുകളും തിരഞ്ഞെടുക്കുക',
        'no_crops': 'അനുയോജ്യമായ വിളകളൊന്നും ഇല്ല',
        'adjust': 'നിങ്ങളുടെ പാരാമീറ്ററുകൾ ക്രമീകരിക്കാൻ ശ്രമിക്കുക',
        'season': 'മികച്ച സീസൺ',
        'water_req': 'ജല ആവശ്യം',
        'duration': 'വളരുന്ന കാലയളവ്',
        'low': 'കുറവ്',
        'medium': 'ഇടത്തരം',
        'high': 'കൂടുതൽ',
        'clay': 'കളിമണ്ണ്',
        'sandy': 'മണൽമണ്ണ്',
        'loamy': 'ലോമി മണ്ണ്',
        'black': 'കറുത്ത മണ്ണ്',
        'red': 'ചുവന്ന മണ്ണ്',
        'alluvial': 'വെള്ളപ്പൊക്ക മണ്ണ്',
    },
    'hi': {
        'title': 'स्मार्ट कृषि फसल योजनाकार 🌾',
        'subtitle': 'डेटा-संचालित अंतर्दृष्टि के साथ अपनी फसलों की योजना बुद्धिमानी से बनाएं',
        'select_language': 'भाषा चुनें',
        'soil_type': 'मिट्टी का प्रकार',
        'rainfall': 'औसत वार्षिक वर्षा (मिमी)',
        'location': 'खेत का स्थान (राज्य)',
        'farm_size': 'खेत का आकार (हेक्टेयर)',
        'get_suggestions': 'फसल सुझाव प्राप्त करें',
        'best_crops': 'आपके खेत के लिए सर्वश्रेष्ठ फसलें',
        'crop': 'फसल',
        'expected_yield': 'अपेक्षित उपज (टन/हेक्टेयर)',
        'profit': 'अनुमानित लाभ (₹/हेक्टेयर)',
        'total_profit': 'कुल अनुमानित लाभ',
        'pest_risk': 'कीट जोखिम',
        'fertilizer': 'अनुशंसित उर्वरक',
        'crop_cycle': 'फसल चक्र कैलेंडर',
        'market_prices': 'औसत बाजार मूल्य',
        'comparison': 'फसल तुलना',
        'price': 'मूल्य (₹/किग्रा)',
        'select_all': 'कृपया सभी विकल्प चुनें',
        'no_crops': 'कोई उपयुक्त फसल नहीं मिली',
        'adjust': 'अपने पैरामीटर समायोजित करने का प्रयास करें',
        'season': 'सर्वोत्तम मौसम',
        'water_req': 'पानी की आवश्यकता',
        'duration': 'बढ़ने की अवधि',
        'low': 'कम',
        'medium': 'मध्यम',
        'high': 'उच्च',
        'clay': 'चिकनी मिट्टी',
        'sandy': 'रेतीली मिट्टी',
        'loamy': 'दोमट मिट्टी',
        'black': 'काली मिट्टी',
        'red': 'लाल मिट्टी',
        'alluvial': 'जलोढ़ मिट्टी',
    }
}

# Initialize database
def init_db():
    """Initialize SQLite database with crop data"""
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()
    
    # Create crops table
    c.execute('''CREATE TABLE IF NOT EXISTS crops
                 (id INTEGER PRIMARY KEY, 
                  name_en TEXT, name_kn TEXT, name_ta TEXT, name_te TEXT, name_ml TEXT, name_hi TEXT,
                  soil_types TEXT, min_rainfall INTEGER, max_rainfall INTEGER,
                  states TEXT, yield_per_hectare REAL, profit_per_hectare INTEGER,
                  pest_risk TEXT, fertilizer TEXT, market_price REAL,
                  season TEXT, water_requirement TEXT, duration_months INTEGER)''')
    
    # Create history table
    c.execute('''CREATE TABLE IF NOT EXISTS search_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT, soil_type TEXT, rainfall INTEGER, location TEXT,
                  farm_size REAL, recommended_crops TEXT)''')
    
    # Check if crops table is empty
    c.execute('SELECT COUNT(*) FROM crops')
    if c.fetchone()[0] == 0:
        # Insert sample crop data
        crops_data = [
            (1, 'Rice', 'ಅಕ್ಕಿ', 'அரிசி', 'వరి', 'അരി', 'चावल',
             'clay,loamy,alluvial', 1000, 2500, 'karnataka,tamilnadu,andhra,telangana,kerala',
             4.5, 45000, 'medium', 'Urea', 35, 'Monsoon', 'High', 5),
            
            (2, 'Wheat', 'ಗೋಧಿ', 'கோதுமை', 'గోధుమ', 'ഗോതമ്പ്', 'गेहूं',
             'loamy,black,alluvial', 400, 900, 'punjab,maharashtra,karnataka',
             3.8, 40000, 'low', 'DAP', 28, 'Winter', 'Medium', 4),
            
            (3, 'Cotton', 'ಹತ್ತಿ', 'பருத்தி', 'పత్తి', 'പഞ്ഞി', 'कपास',
             'black,red,alluvial', 500, 1200, 'maharashtra,karnataka,andhra,telangana',
             2.5, 65000, 'high', 'NPK', 90, 'Kharif', 'Medium', 6),
            
            (4, 'Sugarcane', 'ಕಬ್ಬು', 'கரும்பு', 'చెరకు', 'കരിമ്പ്', 'गन्ना',
             'loamy,clay,black', 1000, 2000, 'maharashtra,karnataka,tamilnadu,andhra',
             70, 120000, 'medium', 'NPK', 3.5, 'Year-round', 'Very High', 12),
            
            (5, 'Maize', 'ಮೆಕ್ಕೆ ಜೋಳ', 'சோளம்', 'మొక్కజొన్న', 'ചോളം', 'मक्का',
             'loamy,sandy,alluvial', 500, 1000, 'karnataka,andhra,telangana,maharashtra',
             5.5, 38000, 'low', 'Urea', 22, 'Kharif', 'Medium', 4),
            
            (6, 'Groundnut', 'ಕಡಲೆಕಾಯಿ', 'நிலக்கடலை', 'వేరుశెనగ', 'നിലക്കടല', 'मूंगफली',
             'sandy,red,black', 500, 1250, 'karnataka,tamilnadu,andhra,telangana',
             1.8, 52000, 'medium', 'Potash', 70, 'Kharif', 'Low', 4),
            
            (7, 'Tomato', 'ಟೊಮೇಟೊ', 'தக்காளி', 'టమాటో', 'തക്കാളി', 'टमाटर',
             'loamy,sandy,red', 600, 1300, 'karnataka,maharashtra,andhra,tamilnadu',
             35, 180000, 'high', 'NPK', 25, 'Winter', 'Medium', 3),
            
            (8, 'Banana', 'ಬಾಳೆಹಣ್ಣು', 'வாழை', 'అరటి', 'വാഴപ്പഴം', 'केला',
             'loamy,alluvial,clay', 1000, 2500, 'kerala,tamilnadu,karnataka,maharashtra',
             40, 250000, 'medium', 'Organic Compost', 30, 'Year-round', 'Very High', 12),
            
            (9, 'Onion', 'ಈರುಳ್ಳಿ', 'வெங்காயம்', 'ఉల్లిపాయ', 'ഉള്ളി', 'प्याज',
             'loamy,sandy,black', 600, 1000, 'maharashtra,karnataka,andhra,tamilnadu',
             25, 95000, 'medium', 'NPK', 35, 'Rabi', 'Medium', 4),
            
            (10, 'Chilli', 'ಮೆಣಸಿನಕಾಯಿ', 'மிளகாய்', 'మిర్చి', 'മുളക്', 'मिर्च',
             'loamy,red,black', 600, 1250, 'andhra,telangana,karnataka,tamilnadu',
             3.5, 85000, 'high', 'NPK', 120, 'Kharif', 'Medium', 5)
        ]
        
        c.executemany('''INSERT INTO crops VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', crops_data)
        conn.commit()
    
    conn.close()

# Load crop data from database
@st.cache_data
def load_crops():
    """Load crops from database"""
    conn = sqlite3.connect('agriculture.db')
    df = pd.read_sql_query("SELECT * FROM crops", conn)
    conn.close()
    return df

# Save search to history
def save_to_history(soil_type, rainfall, location, farm_size, crops):
    """Save search parameters to history"""
    conn = sqlite3.connect('agriculture.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crop_names = ", ".join([c for c in crops])
    c.execute('''INSERT INTO search_history (timestamp, soil_type, rainfall, location, farm_size, recommended_crops)
                 VALUES (?, ?, ?, ?, ?, ?)''', (timestamp, soil_type, rainfall, location, farm_size, crop_names))
    conn.commit()
    conn.close()

# Recommend crops based on inputs
def recommend_crops(df, soil_type, rainfall, location):
    """Filter and recommend crops based on farmer inputs"""
    filtered = df[
        (df['soil_types'].str.contains(soil_type, na=False)) &
        (df['min_rainfall'] <= rainfall) &
        (df['max_rainfall'] >= rainfall) &
        (df['states'].str.contains(location, na=False))
    ]
    return filtered.sort_values('profit_per_hectare', ascending=False)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    # Initialize database
    init_db()
    
    # Load CSS
    load_css()
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Sidebar for language selection and settings
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=100)
        st.title("🌾 Settings")
        
        # Language selector
        lang_options = {
            'English': 'en',
            'ಕನ್ನಡ (Kannada)': 'kn',
            'தமிழ் (Tamil)': 'ta',
            'తెలుగు (Telugu)': 'te',
            'മലയാളം (Malayalam)': 'ml',
            'हिंदी (Hindi)': 'hi'
        }
        
        selected_lang = st.selectbox(
            "🌐 Select Language / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
            options=list(lang_options.keys()),
            index=0
        )
        st.session_state.language = lang_options[selected_lang]
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.write("""
            This Smart Agriculture Crop Planner helps farmers make informed decisions about crop selection.
            
            **Features:**
            - Multi-language support
            - Crop recommendations
            - Profit calculations
            - Pest risk analysis
            - Market price insights
            - Search history tracking
            """)
        
        st.markdown("---")
        st.info("💡 Tip: Use the sliders and dropdowns for easy input!")
    
    # Get translations for selected language
    t = TRANSLATIONS[st.session_state.language]
    
    # Header
    st.title(t['title'])
    st.markdown(f"**{t['subtitle']}**")
    st.markdown("---")
    
    # Load crop database
    crops_df = load_crops()
    
    # Input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        soil_options = {
            t['clay']: 'clay',
            t['sandy']: 'sandy',
            t['loamy']: 'loamy',
            t['black']: 'black',
            t['red']: 'red',
            t['alluvial']: 'alluvial'
        }
        soil_type_display = st.selectbox(
            f"🏞️ {t['soil_type']}",
            options=list(soil_options.keys())
        )
        soil_type = soil_options[soil_type_display]
    
    with col2:
        state_options = {
            'Karnataka / ಕರ್ನಾಟಕ': 'karnataka',
            'Tamil Nadu / தமிழ்நாடு': 'tamilnadu',
            'Andhra Pradesh / ఆంధ్రప్రదేశ్': 'andhra',
            'Telangana / తెలంగాణ': 'telangana',
            'Kerala / കേരളം': 'kerala',
            'Maharashtra / महाराष्ट्र': 'maharashtra',
            'Punjab / ਪੰਜਾਬ': 'punjab'
        }
        location_display = st.selectbox(
            f"📍 {t['location']}",
            options=list(state_options.keys())
        )
        location = state_options[location_display]
    
    with col3:
        farm_size = st.number_input(
            f"📏 {t['farm_size']}",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.5
        )
    
    # Rainfall slider
    st.markdown(f"### 🌧️ {t['rainfall']}")
    rainfall = st.slider("", min_value=200, max_value=3000, value=800, step=50)
    st.info(f"Selected: **{rainfall} mm**")
    
    st.markdown("---")
    
    # Get recommendations button
    if st.button(f"🔍 {t['get_suggestions']}", use_container_width=True):
        with st.spinner('🌱 Finding best crops for you...'):
            recommended = recommend_crops(crops_df, soil_type, rainfall, location)
            
            if len(recommended) > 0:
                # Save to history
                crop_names = recommended[f'name_{st.session_state.language}'].tolist()
                save_to_history(soil_type, rainfall, location, farm_size, crop_names)
                
                # Display results
                st.success(f"✅ Found {len(recommended)} suitable crops!")
                st.markdown(f"## 🌾 {t['best_crops']}")
                
                # Display crop cards
                for idx, row in recommended.head(4).iterrows():
                    with st.expander(f"🌱 {row[f'name_{st.session_state.language}']} - ₹{int(row['profit_per_hectare'] * farm_size):,}", expanded=True):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                t['expected_yield'],
                                f"{row['yield_per_hectare']} t/ha"
                            )
                        
                        with col2:
                            st.metric(
                                t['profit'],
                                f"₹{row['profit_per_hectare']:,}"
                            )
                        
                        with col3:
                            risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                            st.metric(
                                t['pest_risk'],
                                f"{risk_color.get(row['pest_risk'], '⚪')} {t[row['pest_risk']]}"
                            )
                        
                        with col4:
                            st.metric(
                                t['duration'],
                                f"{row['duration_months']} months"
                            )
                        
                        # Additional info
                        col5, col6, col7 = st.columns(3)
                        
                        with col5:
                            st.write(f"**{t['fertilizer']}:** {row['fertilizer']}")
                        
                        with col6:
                            st.write(f"**{t['season']}:** {row['season']}")
                        
                        with col7:
                            st.write(f"**{t['water_req']}:** {row['water_requirement']}")
                        
                        # Total profit calculation
                        total_profit = row['profit_per_hectare'] * farm_size
                        st.success(f"💰 {t['total_profit']}: **₹{int(total_profit):,}** (for {farm_size} hectares)")
                
                st.markdown("---")
                
                # Visualizations
                st.markdown(f"## 📊 {t['comparison']}")
                
                tab1, tab2, tab3 = st.tabs(["📈 Profit Comparison", "🌾 Yield Comparison", "💵 Market Prices"])
                
                with tab1:
                    # Profit bar chart
                    fig_profit = px.bar(
                        recommended.head(5),
                        x=f'name_{st.session_state.language}',
                        y='profit_per_hectare',
                        title=f"{t['profit']} - Top 5 Crops",
                        labels={f'name_{st.session_state.language}': t['crop'], 'profit_per_hectare': t['profit']},
                        color='profit_per_hectare',
                        color_continuous_scale='viridis'
                    )
                    fig_profit.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig_profit, use_container_width=True)
                
                with tab2:
                    # Yield comparison
                    fig_yield = px.bar(
                        recommended.head(5),
                        x=f'name_{st.session_state.language}',
                        y='yield_per_hectare',
                        title=f"{t['expected_yield']} - Top 5 Crops",
                        labels={f'name_{st.session_state.language}': t['crop'], 'yield_per_hectare': t['expected_yield']},
                        color='yield_per_hectare',
                        color_continuous_scale='greens'
                    )
                    fig_yield.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig_yield, use_container_width=True)
                
                with tab3:
                    # Market prices
                    fig_price = px.bar(
                        recommended.head(5),
                        x=f'name_{st.session_state.language}',
                        y='market_price',
                        title=f"{t['market_prices']} - Top 5 Crops",
                        labels={f'name_{st.session_state.language}': t['crop'], 'market_price': t['price']},
                        color='market_price',
                        color_continuous_scale='blues'
                    )
                    fig_price.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig_price, use_container_width=True)
                
                # Pest risk distribution
                st.markdown("### 🐛 Pest Risk Distribution")
                risk_counts = recommended['pest_risk'].value_counts()
                fig_risk = px.pie(
                    values=risk_counts.values,
                    names=[t[risk] for risk in risk_counts.index],
                    title=t['pest_risk'],
                    color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444']
                )
                st.plotly_chart(fig_risk, use_container_width=True)
                
                # Export report
                st.markdown("---")
                st.markdown("### 📥 Export Report")
                
                # Create CSV for export
                export_df = recommended[[f'name_{st.session_state.language}', 'yield_per_hectare', 
                                        'profit_per_hectare', 'pest_risk', 'fertilizer', 'market_price']].head(10)
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="📄 Download Crop Report (CSV)",
                    data=csv,
                    file_name=f"crop_recommendations_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            else:
                st.warning(f"⚠️ {t['no_crops']}")
                st.info(f"💡 {t['adjust']}")
    
    # Search history
    st.markdown("---")
    with st.expander("📜 View Search History"):
        conn = sqlite3.connect('agriculture.db')
        history_df = pd.read_sql_query("SELECT * FROM search_history ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        
        if len(history_df) > 0:
            st.dataframe(history_df[['timestamp', 'soil_type', 'rainfall', 'location', 'recommended_crops']], 
                        use_container_width=True)
        else:
            st.info("No search history yet. Start by getting crop recommendations!")

if __name__ == "__main__":
    main()