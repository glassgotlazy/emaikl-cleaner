import streamlit as st
import random
import string
from datetime import datetime, timedelta
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Terminator Pro - AI-Powered Email Cleaner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ENHANCED CSS with better visibility and effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Animated Matrix Background */
    @keyframes matrix {
        0% { background-position: 0% 0%; }
        100% { background-position: 0% 100%; }
    }
    
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #001a00 50%, #000a00 100%);
        background-size: 100% 200%;
        animation: matrix 20s linear infinite;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, rgba(0, 30, 15, 0.95) 0%, rgba(0, 50, 25, 0.95) 100%);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 
            0 0 100px rgba(0, 255, 65, 0.4),
            inset 0 0 50px rgba(0, 255, 65, 0.1);
        border: 3px solid #00ff41;
    }
    
    /* Glowing animated title */
    @keyframes glow {
        0%, 100% { 
            text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41, 0 0 60px #00ff41;
            filter: brightness(1);
        }
        50% { 
            text-shadow: 0 0 30px #00ff88, 0 0 60px #00ff88, 0 0 90px #00ff88;
            filter: brightness(1.3);
        }
    }
    
    .main-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        color: #00ff41;
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        letter-spacing: 5px;
        animation: glow 2s ease-in-out infinite;
        text-transform: uppercase;
    }
    
    .subtitle {
        text-align: center;
        color: #00ff88;
        font-size: 1.6rem;
        margin-bottom: 3rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.8);
    }
    
    /* Enhanced cyber panels */
    .cyber-panel {
        background: linear-gradient(135deg, rgba(0, 60, 30, 0.7) 0%, rgba(0, 40, 20, 0.7) 100%);
        border: 3px solid #00ff41;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 0 40px rgba(0, 255, 65, 0.5),
            inset 0 0 30px rgba(0, 255, 65, 0.1);
        position: relative;
    }
    
    .cyber-panel::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        box-shadow: 0 0 20px #00ff41;
    }
    
    /* Stat boxes with pulse effect */
    @keyframes pulse {
        0%, 100% { 
            box-shadow: 0 0 25px rgba(0, 255, 65, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 45px rgba(0, 255, 65, 0.7);
            transform: scale(1.02);
        }
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.15) 0%, rgba(0, 255, 136, 0.15) 100%);
        border: 3px solid #00ff41;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        animation: pulse 3s ease-in-out infinite;
        transition: all 0.3s;
    }
    
    .stat-box:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 0 50px rgba(0, 255, 65, 0.8);
    }
    
    .stat-number {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00ff41;
        text-shadow: 0 0 30px rgba(0, 255, 65, 1);
        margin: 1rem 0;
    }
    
    .stat-label {
        color: #00ff88;
        font-size: 1.2rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Enhanced email items */
    @keyframes slideIn {
        from { 
            opacity: 0;
            transform: translateX(-30px);
        }
        to { 
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .email-item {
        background: linear-gradient(135deg, rgba(0, 50, 25, 0.8) 0%, rgba(0, 35, 18, 0.8) 100%);
        border-left: 5px solid #00ff41;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        transition: all 0.3s;
        animation: slideIn 0.5s ease-out;
    }
    
    .email-item:hover {
        background: linear-gradient(135deg, rgba(0, 70, 35, 0.9) 0%, rgba(0, 50, 25, 0.9) 100%);
        border-left-width: 8px;
        transform: translateX(15px) scale(1.02);
        box-shadow: 0 0 35px rgba(0, 255, 65, 0.6);
    }
    
    .email-subject {
        color: #00ff41;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    .email-sender {
        color: #00ff88;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .email-date {
        color: #00ffaa;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .email-preview {
        color: #00cc66;
        font-size: 0.95rem;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(0, 255, 65, 0.3);
        font-style: italic;
    }
    
    /* Badges */
    .spam-badge {
        background: linear-gradient(135deg, #ff0000 0%, #ff3333 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
        display: inline-block;
        margin-left: 10px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .category-badge {
        background: linear-gradient(135deg, #ff8800 0%, #ffaa00 100%);
        color: #000;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin: 0 5px;
        box-shadow: 0 0 10px rgba(255, 136, 0, 0.6);
    }
    
    /* Buttons with glow */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00ff41 0%, #00ff88 100%);
        color: #000000;
        border: none;
        border-radius: 12px;
        padding: 1.2rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 900;
        letter-spacing: 3px;
        text-transform: uppercase;
        transition: all 0.3s;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
        font-family: 'Orbitron', sans-serif;
        border: 2px solid transparent;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 0 50px rgba(0, 255, 65, 0.9);
        background: linear-gradient(135deg, #00ff88 0%, #00ffdd 100%);
        border-color: #00ff41;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(0, 50, 25, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        border: 2px solid rgba(0, 255, 65, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 16px 32px;
        font-weight: 900;
        color: #00ff41;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 65, 0.1);
        border-color: #00ff41;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff41 0%, #00ff88 100%) !important;
        color: #000000 !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.7);
        border-color: #00ff41 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        color: #00ff41 !important;
        text-shadow: 0 0 25px rgba(0, 255, 65, 1);
    }
    
    [data-testid="stMetricLabel"] {
        color: #00ff88 !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1rem !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff41 0%, #00ff88 50%, #00ffdd 100%);
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.8);
    }
    
    /* Alerts */
    .stSuccess {
        background: rgba(0, 255, 65, 0.2) !important;
        border: 3px solid #00ff41 !important;
        border-radius: 12px !important;
        color: #00ff41 !important;
        font-weight: 700 !important;
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.4);
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.2) !important;
        border: 3px solid #ffaa00 !important;
        border-radius: 12px !important;
        color: #ffaa00 !important;
        font-weight: 700 !important;
    }
    
    .stInfo {
        background: rgba(0, 200, 255, 0.2) !important;
        border: 3px solid #00ccff !important;
        border-radius: 12px !important;
        color: #00ccff !important;
        font-weight: 700 !important;
    }
    
    .stError {
        background: rgba(255, 0, 0, 0.2) !important;
        border: 3px solid #ff0000 !important;
        border-radius: 12px !important;
        color: #ff4444 !important;
        font-weight: 700 !important;
    }
    
    /* Form elements */
    .stSelectbox > div > div,
    .stTextArea textarea,
    .stTextInput input,
    .stNumberInput input {
        background: rgba(0, 50, 25, 0.8) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        color: #00ff41 !important;
        font-weight: 600 !important;
    }
    
    .stCheckbox {
        color: #00ff88 !important;
        font-weight: 700 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 3px solid #00ff41 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.15) 0%, rgba(0, 255, 136, 0.15) 100%);
        border: 2px solid #00ff41;
        border-radius: 12px;
        font-weight: 900;
        font-size: 1.1rem;
        padding: 1.2rem;
        color: #00ff41 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff41 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.6) !important;
    }
    
    /* Paragraphs and lists */
    p, li, span {
        color: #00ff88 !important;
        font-weight: 600 !important;
    }
    
    /* Code blocks */
    code {
        font-family: 'Orbitron', monospace !important;
        background: rgba(0, 255, 65, 0.15) !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        color: #00ff41 !important;
        border: 2px solid rgba(0, 255, 65, 0.4) !important;
        font-weight: 700 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 255, 65, 0.3) !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'total_emails' not in st.session_state:
    st.session_state.total_emails = 0
if 'spam_detected' not in st.session_state:
    st.session_state.spam_detected = 0
if 'deleted' not in st.session_state:
    st.session_state.deleted = 0
if 'deleted_emails' not in st.session_state:
    st.session_state.deleted_emails = []
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'last_scan' not in st.session_state:
    st.session_state.last_scan = None

# Enhanced demo spam emails with more details
DEMO_SPAM = [
    {
        "subject": "CONGRATULATIONS! You've won $1,000,000 💰",
        "sender": "lottery@fake-winner.com",
        "date": "2 hours ago",
        "spam_score": 98,
        "category": "Scam",
        "preview": "Click here to claim your prize! You are the lucky winner of our international lottery...",
        "size": "12 KB",
        "attachments": 0
    },
    {
        "subject": "Enlarge your... [SPAM DETECTED]",
        "sender": "pills@spam-mail.net",
        "date": "3 hours ago",
        "spam_score": 99,
        "category": "Adult",
        "preview": "Special offer on enhancement pills. 100% natural and guaranteed results...",
        "size": "8 KB",
        "attachments": 1
    },
    {
        "subject": "🎁 FREE iPhone 15 Pro Max - Limited Time!",
        "sender": "promo@scam-offers.biz",
        "date": "5 hours ago",
        "spam_score": 95,
        "category": "Phishing",
        "preview": "You've been selected! Click now to claim your free iPhone. Only 10 left in stock...",
        "size": "15 KB",
        "attachments": 2
    },
    {
        "subject": "🚨 URGENT: Your package delivery failed",
        "sender": "delivery@phishing-site.ru",
        "date": "1 day ago",
        "spam_score": 92,
        "category": "Phishing",
        "preview": "Your package could not be delivered. Update your address immediately or it will be returned...",
        "size": "10 KB",
        "attachments": 0
    },
    {
        "subject": "Meet hot singles in your area NOW 🔥",
        "sender": "dating@spam-central.org",
        "date": "1 day ago",
        "spam_score": 97,
        "category": "Adult",
        "preview": "Thousands of singles waiting to meet you. Sign up now for free and start chatting...",
        "size": "18 KB",
        "attachments": 3
    },
    {
        "subject": "💰 WORK FROM HOME - Earn $5000/week!",
        "sender": "jobs@mlm-scam.info",
        "date": "2 days ago",
        "spam_score": 94,
        "category": "Scam",
        "preview": "No experience needed! Start earning today with our proven system. Join 10,000+ members...",
        "size": "14 KB",
        "attachments": 1
    },
    {
        "subject": "⚠️ PayPal: Account will be suspended!",
        "sender": "security@fake-paypal.com",
        "date": "2 days ago",
        "spam_score": 96,
        "category": "Phishing",
        "preview": "Suspicious activity detected. Verify your identity within 24 hours or lose access...",
        "size": "11 KB",
        "attachments": 0
    },
    {
        "subject": "Re: Invoice #12345 [VIRUS WARNING]",
        "sender": "billing@malware-sender.tk",
        "date": "3 days ago",
        "spam_score": 100,
        "category": "Malware",
        "preview": "Please see attached invoice for payment. Download and open the PDF to view details...",
        "size": "25 KB",
        "attachments": 1
    },
]

# Title
st.markdown('<h1 class="main-title">🛡️ GMAIL SPAM TERMINATOR PRO</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">⚡ Advanced AI-Powered Email Security System</p>', unsafe_allow_html=True)

# Sidebar - Enhanced Gmail Connection
with st.sidebar:
    st.markdown("### 🔐 Gmail Connection")
    
    st.info("""
    **📝 Quick Setup:**
    
    1. Go to [Google Cloud Console](https://console.cloud.google.com)
    2. Enable Gmail API
    3. Download credentials.json
    4. Upload here & authorize
    
    [📖 Detailed Guide](https://developers.google.com/gmail/api/quickstart/python)
    """)
    
    uploaded_creds = st.file_uploader(
        "📁 Upload credentials.json",
        type=['json'],
        help="Gmail API credentials file"
    )
    
    if uploaded_creds and not st.session_state.connected:
        if st.button("🔗 CONNECT TO GMAIL", type="primary", use_container_width=True):
            with st.spinner("🔐 Establishing secure connection..."):
                import time
                time.sleep(2)
                st.session_state.connected = True
                st.session_state.total_emails = random.randint(800, 2500)
                st.session_state.spam_detected = len(DEMO_SPAM)
                st.success("✅ Connected successfully!")
                st.balloons()
                st.rerun()
    
    if st.session_state.connected:
        st.success("✅ **CONNECTED**")
        
        if st.session_state.last_scan:
            st.info(f"🕒 Last scan: {st.session_state.last_scan}")
        
        st.markdown("---")
        st.markdown("### ⚙️ Advanced Settings")
        
        auto_delete = st.checkbox("🗑️ Auto-Delete Spam", value=True)
        sensitivity = st.slider("🎯 Detection Sensitivity", 1, 10, 8)
        backup_deleted = st.checkbox("💾 Backup Before Delete", value=True)
        notify_spam = st.checkbox("🔔 Notify on Spam", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Scans", st.session_state.scan_count)
        st.metric("Emails Deleted", st.session_state.deleted)
        
        st.markdown("---")
        
        if st.button("🔌 DISCONNECT", use_container_width=True):
            st.session_state.connected = False
            st.rerun()

# Main content
if not st.session_state.connected:
    # Enhanced landing page
    st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Welcome to the Ultimate Email Protection System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ⚡ Core Features:
        - 🤖 **AI-Powered Detection** - Machine learning spam classifier
        - 🗑️ **Smart Auto-Delete** - Automatic spam removal
        - 📊 **Real-Time Analytics** - Live inbox monitoring
        - 🔒 **OAuth2 Security** - Bank-grade encryption
        - ⚡ **Bulk Operations** - Process thousands of emails
        - 📈 **Detailed Reports** - Comprehensive analytics
        - 🎯 **Custom Filters** - Personalized rules
        - 💾 **Backup System** - Recover deleted emails
        - 🔍 **Advanced Search** - Find anything instantly
        - 📧 **Email Preview** - See before you delete
        """)
    
    with col2:
        st.markdown("""
        #### 🛡️ Security & Safety:
        - ✅ **Read-Only Mode** - Safe by default
        - ✅ **Manual Approval** - Review before delete
        - ✅ **30-Day Undo** - Recover from trash
        - ✅ **Encrypted API** - Secure connections
        - ✅ **Zero Storage** - No data kept
        - ✅ **Open Source** - Transparent code
        - ✅ **GDPR Compliant** - Privacy protected
        - ✅ **2FA Support** - Extra security layer
        - ✅ **Audit Logs** - Track all actions
        - ✅ **Multi-Account** - Manage multiple emails
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Why Choose Spam Terminator Pro?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🚀 Speed**
        - Process 1000+ emails/min
        - Real-time scanning
        - Instant results
        """)
    
    with col2:
        st.markdown("""
        **🎯 Accuracy**
        - 99.8% detection rate
        - AI-powered learning
        - Minimal false positives
        """)
    
    with col3:
        st.markdown("""
        **💰 Cost**
        - 100% Free forever
        - No hidden fees
        - Unlimited usage
        """)
    
    st.markdown("---")
    
    st.warning("""
    **⚠️ Important Setup Information:**
    
    This is a demo UI showcasing the complete feature set. To connect to real Gmail:
    
    **Step 1: Enable Gmail API**
    1. Visit [Google Cloud Console](https://console.cloud.google.com)
    2. Create new project or select existing
    3. Enable Gmail API
    4. Create OAuth 2.0 credentials
    5. Download credentials.json
    
    **Step 2: Install Dependencies**
    ```
    pip install google-auth google-auth-oauthlib google-api-python-client
    ```
    
    **Step 3: Implement OAuth Flow**
    ```
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    # Authenticate
    service = build('gmail', 'v1', credentials=creds)
    
    # List spam emails
    results = service.users().messages().list(
        userId='me', 
        q='is:spam',
        maxResults=100
    ).execute()
    
    # Delete spam
    service.users().messages().trash(
        userId='me',
        id=message_id
    ).execute()
    ```
    
    [📖 Full Documentation](https://developers.google.com/gmail/api)
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Main dashboard with enhanced features
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 DASHBOARD", 
        "🗑️ SPAM CLEANER", 
        "📈 ANALYTICS", 
        "⚙️ FILTERS",
        "🗂️ DELETED HISTORY",
        "🔧 TOOLS"
    ])
    
    # TAB 1: Enhanced Dashboard
    with tab1:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📊 Real-Time Inbox Monitor")
        
        # Top stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.total_emails}</div>
                <div class="stat-label">📬 Total Emails</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.spam_detected}</div>
                <div class="stat-label">🚨 Spam Detected</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.deleted}</div>
                <div class="stat-label">🗑️ Deleted</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            clean_percent = ((st.session_state.total_emails - st.session_state.spam_detected) / st.session_state.total_emails * 100) if st.session_state.total_emails > 0 else 100
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{clean_percent:.1f}%</div>
                <div class="stat-label">✨ Clean Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Additional metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⚡ Processing Speed", "1,243 emails/min")
        with col2:
            st.metric("🎯 Accuracy Rate", "99.8%")
        with col3:
            storage_saved = st.session_state.deleted * 0.015  # Avg 15KB per email
            st.metric("💾 Storage Saved", f"{storage_saved:.1f} MB")
        with col4:
            time_saved = st.session_state.deleted * 0.5  # Avg 30s per email
            st.metric("⏱️ Time Saved", f"{int(time_saved)} min")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 DEEP SCAN", use_container_width=True):
                with st.spinner("🔍 Deep scanning inbox..."):
                    progress = st.progress(0)
                    for i in range(100):
                        import time
                        time.sleep(0.02)
                        progress.progress(i + 1)
                    st.session_state.scan_count += 1
                    st.session_state.last_scan = datetime.now().strftime("%I:%M %p")
                    st.success(f"✅ Scan complete! Found {len(DEMO_SPAM)} spam emails")
                    st.balloons()
        
        with col2:
            if st.button("🗑️ DELETE ALL", use_container_width=True):
                if st.session_state.spam_detected > 0:
                    st.session_state.deleted_emails.extend(DEMO_SPAM[:st.session_state.spam_detected])
                    st.session_state.deleted += st.session_state.spam_detected
                    st.session_state.spam_detected = 0
                    st.success(f"✅ Deleted {len(DEMO_SPAM)} spam emails!")
                    st.rerun()
                else:
                    st.info("No spam to delete")
        
        with col3:
            if st.button("📥 EXPORT REPORT", use_container_width=True):
                report_data = {
                    "scan_date": datetime.now().isoformat(),
                    "total_emails": st.session_state.total_emails,
                    "spam_detected": len(DEMO_SPAM),
                    "emails_deleted": st.session_state.deleted,
                    "clean_rate": clean_percent,
                    "spam_list": DEMO_SPAM
                }
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "📊 Download JSON",
                        json.dumps(report_data, indent=2),
                        "spam_report.json",
                        "application/json",
                        use_container_width=True
                    )
                with col_b:
                    df_report = pd.DataFrame(DEMO_SPAM)
                    st.download_button(
                        "📊 Download CSV",
                        df_report.to_csv(index=False),
                        "spam_report.csv",
                        "text/csv",
                        use_container_width=True
                    )
        
        with col4:
            if st.button("🔄 REFRESH DATA", use_container_width=True):
                st.rerun()
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### 📋 Recent Activity")
        
        activity_log = [
            {"time": "2 min ago", "action": "Detected 8 spam emails", "icon": "🔍"},
            {"time": "15 min ago", "action": "Deleted 12 phishing attempts", "icon": "🗑️"},
            {"time": "1 hour ago", "action": "Blocked suspicious sender", "icon": "🚫"},
            {"time": "2 hours ago", "action": "Updated spam filters", "icon": "⚙️"},
        ]
        
        for log in activity_log:
            st.info(f"{log['icon']} **{log['action']}** - _{log['time']}_")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: Enhanced Spam Cleaner with full details
    with tab2:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 🗑️ Spam Email Manager")
        
        if st.session_state.spam_detected == 0:
            st.success("✨ **Your inbox is pristine!** No spam detected.")
            st.info("💡 Run a scan from the Dashboard to check for new spam")
        else:
            st.warning(f"⚠️ **{len(DEMO_SPAM)} spam emails** detected and ready for removal")
            
            # Bulk actions
            col1, col2, col3 = st.columns(3)
            with col1:
                select_all = st.checkbox("Select All", value=True)
            with col2:
                if st.button("🗑️ Delete Selected", type="primary", use_container_width=True):
                    st.success("Deleted selected emails!")
            with col3:
                if st.button("✅ Mark as Safe", use_container_width=True):
                    st.info("Marked as safe")
            
            st.markdown("---")
            
            # Display each spam email with full details
            for idx, email in enumerate(DEMO_SPAM):
                st.markdown(f"""
                <div class="email-item">
                    <div class="email-subject">
                        {email['subject']}
                        <span class="spam-badge">🚨 SPAM {email['spam_score']}%</span>
                        <span class="category-badge">{email['category']}</span>
                    </div>
                    <div class="email-sender">
                        📧 From: {email['sender']}
                    </div>
                    <div class="email-date">
                        🕒 {email['date']} | 📦 Size: {email['size']} | 📎 Attachments: {email['attachments']}
                    </div>
                    <div class="email-preview">
                        📝 Preview: {email['preview']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col2:
                    if st.button(f"👁️ View Full", key=f"view_{idx}", use_container_width=True):
                        with st.expander("Full Email Details", expanded=True):
                            st.markdown(f"""
                            **Subject:** {email['subject']}  
                            **From:** {email['sender']}  
                            **Date:** {email['date']}  
                            **Spam Score:** {email['spam_score']}%  
                            **Category:** {email['category']}  
                            **Size:** {email['size']}  
                            **Attachments:** {email['attachments']}  
                            
                            **Preview:**  
                            {email['preview']}
                            
                            ---
                            
                            **Why flagged as spam:**
                            - Suspicious sender domain
                            - Contains promotional keywords
                            - Excessive use of capital letters
                            - Suspicious links detected
                            """)
                
                with col3:
                    if st.button(f"✅ Not Spam", key=f"keep_{idx}", use_container_width=True):
                        st.info(f"✅ Moved to inbox: {email['subject'][:40]}...")
                
                with col4:
                    if st.button(f"🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                        st.session_state.deleted_emails.append(email)
                        st.session_state.deleted += 1
                        st.success(f"🗑️ Deleted: {email['subject'][:40]}...")
                
                if idx < len(DEMO_SPAM) - 1:
                    st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Advanced Analytics
    with tab3:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📈 Comprehensive Spam Analytics")
        
        # Spam categories
        df_categories = pd.DataFrame({
            'Category': ['Phishing', 'Marketing', 'Malware', 'Scam', 'Adult', 'Other'],
            'Count': [28, 52, 15, 22, 12, 18],
            'Percentage': [19, 35, 10, 15, 8, 12],
            'Risk Level': ['🔴 High', '🟡 Medium', '🔴 High', '🔴 High', '🟠 Medium', '🟢 Low']
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Spam by Category")
            st.dataframe(df_categories, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🎯 Top Spam Senders")
            top_senders = pd.DataFrame({
                'Sender Domain': ['fake-winner.com', 'spam-mail.net', 'scam-offers.biz', 'phishing-site.ru'],
                'Spam Count': [52, 45, 38, 34],
                'Blocked': ['✅', '✅', '✅', '✅']
            })
            st.dataframe(top_senders, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Spam Trend (Last 7 Days)")
            trend_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Spam Received': [15, 22, 18, 28, 24, 10, 8],
                'Deleted': [14, 21, 17, 27, 23, 9, 7]
            })
            st.line_chart(trend_data.set_index('Day'))
        
        with col2:
            st.markdown("#### 🕒 Spam by Time of Day")
            time_data = pd.DataFrame({
                'Hour': ['00-06', '06-12', '12-18', '18-24'],
                'Count': [8, 35, 52, 30]
            })
            st.bar_chart(time_data.set_index('Hour'))
        
        st.markdown("---")
        
        st.markdown("#### 🌍 Spam Origins (Geographic)")
        
        origin_data = pd.DataFrame({
            'Country': ['Russia', 'China', 'Nigeria', 'USA', 'India', 'Others'],
            'Spam Count': [45, 38, 28, 15, 12, 25],
            'Percentage': [27.6, 23.3, 17.2, 9.2, 7.4, 15.3]
        })
        
        st.dataframe(origin_data, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 4: Advanced Filters
    with tab4:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Advanced Spam Filtering System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚫 Blocked Keywords")
            blocked_keywords = st.text_area(
                "Enter keywords to block (one per line):",
                value="viagra\ncasino\nfree money\nclick here\nurgent\nact now\nwinner\nlottery\npills\ncongratulations",
                height=200
            )
        
        with col2:
            st.markdown("#### 📧 Blocked Senders")
            blocked_senders = st.text_area(
                "Enter email addresses/domains to block:",
                value="spam@example.com\nscam@fake.net\n*.ru\n*.tk\nfake-winner.com",
                height=200
            )
        
        st.markdown("---")
        
        st.markdown("#### 🎯 Advanced Detection Rules")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.checkbox("Block excessive capitals (>50%)", value=True)
            st.checkbox("Block suspicious links", value=True)
            st.checkbox("Block unknown senders", value=False)
            st.checkbox("Block forwarded emails", value=False)
        
        with col2:
            st.checkbox("Block attachments from unknown", value=True)
            st.checkbox("Block emails with $$$$ symbols", value=True)
            st.checkbox("Block no unsubscribe link", value=False)
            st.checkbox("Block HTML-only emails", value=False)
        
        with col3:
            st.checkbox("Block multiple recipients", value=False)
            st.checkbox("Block suspicious URLs", value=True)
            st.checkbox("Block executables (.exe, .bat)", value=True)
            st.checkbox("Block foreign languages", value=False)
        
        st.markdown("---")
        
        st.markdown("#### 🔍 Whitelist Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            safe_senders = st.text_area(
                "Always allow emails from:",
                value="company@work.com\nfriend@gmail.com\nbank@chase.com",
                height=150
            )
        
        with col2:
            safe_domains = st.text_area(
                "Trusted domains:",
                value="*.gov\n*.edu\n*.org\ngoogle.com\nmicrosoft.com",
                height=150
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 SAVE FILTERS", type="primary", use_container_width=True):
                st.success("✅ Filters saved and applied!")
        
        with col2:
            if st.button("🔄 RESET TO DEFAULT", use_container_width=True):
                st.info("Reset to default settings")
        
        with col3:
            if st.button("📥 EXPORT RULES", use_container_width=True):
                rules = {
                    "blocked_keywords": blocked_keywords.split('\n'),
                    "blocked_senders": blocked_senders.split('\n'),
                    "safe_senders": safe_senders.split('\n')
                }
                st.download_button(
                    "Download Rules",
                    json.dumps(rules, indent=2),
                    "filter_rules.json",
                    "application/json"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 5: Deleted Email History
    with tab5:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 🗂️ Deleted Email History")
        
        if len(st.session_state.deleted_emails) == 0:
            st.info("📭 No deleted emails yet")
        else:
            st.success(f"📊 Total deleted: {len(st.session_state.deleted_emails)} emails")
            
            # Actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 RESTORE ALL", use_container_width=True):
                    st.session_state.deleted_emails = []
                    st.success("Restored all emails!")
                    st.rerun()
            with col2:
                if st.button("🗑️ EMPTY TRASH", use_container_width=True):
                    st.session_state.deleted_emails = []
                    st.warning("Trash emptied permanently!")
                    st.rerun()
            with col3:
                if st.button("📥 EXPORT LIST", use_container_width=True):
                    df_deleted = pd.DataFrame(st.session_state.deleted_emails)
                    st.download_button(
                        "Download",
                        df_deleted.to_csv(index=False),
                        "deleted_emails.csv",
                        "text/csv"
                    )
            
            st.markdown("---")
            
            # Display deleted emails
            for idx, email in enumerate(st.session_state.deleted_emails):
                st.markdown(f"""
                <div class="email-item">
                    <div class="email-subject">
                        🗑️ {email['subject']}
                    </div>
                    <div class="email-sender">From: {email['sender']}</div>
                    <div class="email-date">Deleted: {email['date']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col2:
                    if st.button(f"🔄 Restore", key=f"restore_{idx}", use_container_width=True):
                        st.success(f"Restored: {email['subject'][:30]}...")
                with col3:
                    if st.button(f"❌ Delete Forever", key=f"permanent_{idx}", use_container_width=True):
                        st.warning(f"Permanently deleted!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 6: Additional Tools
    with tab6:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 🔧 Email Management Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📧 Bulk Email Search")
            search_query = st.text_input("Search emails:", placeholder="Enter keywords, sender, subject...")
            date_range = st.date_input("Date range:", [])
            
            if st.button("🔍 SEARCH", use_container_width=True):
                st.info(f"Searching for: {search_query}")
        
        with col2:
            st.markdown("#### 🏷️ Label Management")
            label_name = st.text_input("Create new label:", placeholder="e.g., Important, Work, Personal")
            label_color = st.selectbox("Label color:", ["🔴 Red", "🟢 Green", "🔵 Blue", "🟡 Yellow", "🟣 Purple"])
            
            if st.button("➕ CREATE LABEL", use_container_width=True):
                st.success(f"Created label: {label_name}")
        
        st.markdown("---")
        
        st.markdown("#### 📊 Storage Analyzer")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📦 Total Storage", "12.5 GB / 15 GB")
        with col2:
            st.metric("📧 Email Storage", "8.2 GB")
        with col3:
            st.metric("📎 Attachments", "4.3 GB")
        
        st.progress(0.83)
        
        if st.button("🗑️ CLEAN LARGE EMAILS", type="primary", use_container_width=True):
            st.info("Finding emails larger than 10 MB...")
        
        st.markdown("---")
        
        st.markdown("#### 🔐 Security Scan")
        
        if st.button("🛡️ RUN SECURITY SCAN", use_container_width=True):
            with st.spinner("Scanning for security threats..."):
                import time
                time.sleep(2)
                st.success("✅ No security threats detected!")
                st.info("📊 Scan Results:")
                st.write("- Phishing attempts blocked: 12")
                st.write("- Malware attachments removed: 3")
                st.write("- Suspicious links detected: 8")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem; 
background: linear-gradient(135deg, rgba(0, 60, 30, 0.8) 0%, rgba(0, 40, 20, 0.8) 100%); 
border: 3px solid #00ff41;
border-radius: 20px; 
box-shadow: 0 0 50px rgba(0, 255, 65, 0.5);">
    <div style="font-size: 2.8rem; font-weight: 900; color: #00ff41; margin-bottom: 1.5rem; 
    font-family: 'Orbitron', sans-serif; text-shadow: 0 0 30px rgba(0, 255, 65, 1);">
        🛡️ GMAIL SPAM TERMINATOR PRO
    </div>
    <div style="font-size: 1.4rem; color: #00ff88; font-weight: 700; margin-bottom: 1rem;">
        Made with ❤️ using Streamlit & Gmail API
    </div>
    <div style="font-size: 1.2rem; color: #00ffaa; margin-bottom: 2rem;">
        🔒 Secure • ⚡ Fast • 🎯 Accurate • 🤖 AI-Powered • 💯 Free
    </div>
    <div style="font-size: 1rem; color: #00cc88; font-weight: 600;">
        ✨ Protect Your Inbox • Delete Spam Automatically • Stay Organized • Save Time ✨
    </div>
    <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 2px solid rgba(0, 255, 65, 0.3);">
        <span style="color: #00ff88; font-size: 0.95rem;">
            📊 {st.session_state.total_emails} Emails Processed | 
            🗑️ {st.session_state.deleted} Spam Deleted | 
            ⚡ {st.session_state.scan_count} Scans Performed
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
