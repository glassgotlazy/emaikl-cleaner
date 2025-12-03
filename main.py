import streamlit as st
import base64
from datetime import datetime
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Sorter & Cleaner - Auto Delete Spam Emails",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Free Gmail spam sorter and cleaner. Automatically detect and delete spam emails. Clean your inbox instantly. Smart AI-powered spam detection.">
<meta name="keywords" content="gmail spam filter, delete spam emails, gmail cleaner, inbox organizer, auto delete spam, email sorter">
""", unsafe_allow_html=True)

# Futuristic Cyberpunk CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Matrix-style background */
    .stApp {
        background: #000000;
        position: relative;
        overflow: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(90deg, transparent 0%, rgba(0, 255, 65, 0.03) 50%, transparent 100%),
            repeating-linear-gradient(0deg, rgba(0, 255, 65, 0.05) 0px, transparent 2px, transparent 4px, rgba(0, 255, 65, 0.05) 6px);
        pointer-events: none;
        z-index: 0;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, rgba(0, 20, 10, 0.95) 0%, rgba(10, 30, 20, 0.95) 100%);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 
            0 0 100px rgba(0, 255, 65, 0.3),
            inset 0 0 50px rgba(0, 255, 65, 0.05);
        border: 2px solid rgba(0, 255, 65, 0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Glowing title */
    .main-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #00ff41 0%, #00ff88 50%, #00ffdd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 0 0 50px rgba(0, 255, 65, 0.8);
        letter-spacing: 5px;
        animation: titleGlow 2s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 20px rgba(0, 255, 65, 0.8)); }
        50% { filter: brightness(1.5) drop-shadow(0 0 40px rgba(0, 255, 65, 1)); }
    }
    
    .subtitle {
        text-align: center;
        color: #00ff41;
        font-size: 1.6rem;
        margin-bottom: 3rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* Cyber panels */
    .cyber-panel {
        background: linear-gradient(135deg, rgba(0, 50, 25, 0.8) 0%, rgba(0, 30, 15, 0.8) 100%);
        border: 2px solid #00ff41;
        border-radius: 15px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.4),
            inset 0 0 30px rgba(0, 255, 65, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .cyber-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ff41, transparent, #00ff88, transparent);
        border-radius: 15px;
        opacity: 0;
        transition: opacity 0.3s;
        z-index: -1;
    }
    
    .cyber-panel:hover::before {
        opacity: 0.3;
        animation: borderGlow 2s linear infinite;
    }
    
    @keyframes borderGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Holographic buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00ff41 0%, #00ff88 100%);
        color: #000000;
        border: none;
        border-radius: 10px;
        padding: 1.3rem 2.5rem;
        font-size: 1.3rem;
        font-weight: 900;
        letter-spacing: 3px;
        text-transform: uppercase;
        transition: all 0.3s;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.6),
            inset 0 0 20px rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        font-family: 'Orbitron', sans-serif;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 0 50px rgba(0, 255, 65, 0.9),
            inset 0 0 30px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #00ff88 0%, #00ffdd 100%);
    }
    
    /* Stats display */
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.1) 0%, rgba(0, 255, 136, 0.1) 100%);
        border: 2px solid #00ff41;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            0 0 25px rgba(0, 255, 65, 0.3),
            inset 0 0 20px rgba(0, 255, 65, 0.05);
        transition: all 0.3s;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 40px rgba(0, 255, 65, 0.5);
    }
    
    .stat-number {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff41 0%, #00ffdd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 255, 65, 0.8);
        margin: 1rem 0;
    }
    
    .stat-label {
        color: #00ff88;
        font-size: 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Email list */
    .email-item {
        background: rgba(0, 40, 20, 0.6);
        border-left: 4px solid #00ff41;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .email-item:hover {
        background: rgba(0, 50, 25, 0.8);
        border-left-width: 6px;
        transform: translateX(10px);
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.4);
    }
    
    .email-subject {
        color: #00ff41;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .email-sender {
        color: #00ff88;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    .email-date {
        color: #00ffaa;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .spam-badge {
        background: linear-gradient(135deg, #ff0000 0%, #ff4444 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.6);
        display: inline-block;
        margin-left: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(0, 40, 20, 0.5);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 65, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: 900;
        color: #00ff41;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.3s;
        font-family: 'Orbitron', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 65, 0.1);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff41 0%, #00ff88 100%) !important;
        color: #000000 !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff41 0%, #00ffdd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        color: #00ff88 !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff41 0%, #00ff88 100%);
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
    }
    
    /* Alert boxes */
    .stSuccess {
        background: rgba(0, 255, 65, 0.1) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        color: #00ff41 !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.1) !important;
        border: 2px solid #ffaa00 !important;
        border-radius: 10px !important;
        color: #ffaa00 !important;
    }
    
    .stError {
        background: rgba(255, 0, 0, 0.1) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 10px !important;
        color: #ff4444 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(0, 40, 20, 0.8);
        border: 2px solid #00ff41;
        border-radius: 10px;
        color: #00ff41;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #00ff88 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 2px solid #00ff41;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.3);
    }
    
    /* Scanner animation */
    @keyframes scan {
        0%, 100% { transform: translateY(-100%); }
        50% { transform: translateY(100%); }
    }
    
    .scanner {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        box-shadow: 0 0 20px #00ff41;
        animation: scan 3s linear infinite;
    }
    
    /* Terminal text */
    code {
        font-family: 'Orbitron', monospace;
        background: rgba(0, 255, 65, 0.1);
        padding: 4px 8px;
        border-radius: 5px;
        color: #00ff41;
        border: 1px solid rgba(0, 255, 65, 0.3);
    }
    
    h3 {
        color: #00ff41 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    p, li {
        color: #00ff88 !important;
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

# Demo spam emails
DEMO_SPAM = [
    {"subject": "CONGRATULATIONS! You've won $1,000,000", "sender": "lottery@fake-winner.com", "date": "2 hours ago", "spam_score": 98},
    {"subject": "Enlarge your... [SPAM]", "sender": "pills@spam-mail.net", "date": "3 hours ago", "spam_score": 99},
    {"subject": "Click here for FREE iPhone 15!", "sender": "promo@scam-offers.biz", "date": "5 hours ago", "spam_score": 95},
    {"subject": "Your package is waiting - URGENT", "sender": "delivery@phishing-site.ru", "date": "1 day ago", "spam_score": 92},
    {"subject": "Meet hot singles in your area NOW", "sender": "dating@spam-central.org", "date": "1 day ago", "spam_score": 97},
    {"subject": "WORK FROM HOME $$$$$", "sender": "jobs@mlm-scam.info", "date": "2 days ago", "spam_score": 94},
    {"subject": "Your account will be suspended!", "sender": "security@fake-paypal.com", "date": "2 days ago", "spam_score": 96},
    {"subject": "Re: Invoice #12345 [VIRUS DETECTED]", "sender": "billing@malware-sender.tk", "date": "3 days ago", "spam_score": 100},
]

# Title
st.markdown('<h1 class="main-title">🛡️ GMAIL SPAM TERMINATOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">⚡ AI-Powered Spam Detection & Auto-Delete System</p>', unsafe_allow_html=True)

# Sidebar - Gmail Connection
with st.sidebar:
    st.markdown("### 🔐 Gmail Connection")
    
    st.info("""
    **📝 Setup Instructions:**
    
    1. Enable Gmail API in Google Cloud Console
    2. Download credentials.json
    3. Upload credentials here
    4. Authorize access
    
    [📖 Full Guide](https://developers.google.com/gmail/api/quickstart/python)
    """)
    
    uploaded_creds = st.file_uploader(
        "Upload credentials.json",
        type=['json'],
        help="Gmail API credentials file"
    )
    
    if uploaded_creds and not st.session_state.connected:
        if st.button("🔗 CONNECT TO GMAIL", type="primary", use_container_width=True):
            with st.spinner("Establishing secure connection..."):
                import time
                time.sleep(2)
                st.session_state.connected = True
                st.session_state.total_emails = random.randint(500, 2000)
                st.session_state.spam_detected = len(DEMO_SPAM)
                st.success("✅ Connected!")
                st.rerun()
    
    if st.session_state.connected:
        st.success("✅ **Connected**")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        auto_delete = st.checkbox("🗑️ Auto-Delete Spam", value=True)
        sensitivity = st.slider("Detection Sensitivity", 1, 10, 8)
        
        st.markdown("---")
        
        if st.button("🔌 DISCONNECT", use_container_width=True):
            st.session_state.connected = False
            st.rerun()

# Main content
if not st.session_state.connected:
    # Landing page
    st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Welcome to Gmail Spam Terminator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ⚡ Features:
        - 🤖 AI-Powered spam detection
        - 🗑️ Auto-delete spam emails
        - 📊 Real-time analytics
        - 🔒 Secure OAuth2 authentication
        - ⚡ Lightning-fast processing
        - 📈 Detailed spam reports
        - 🎯 Customizable filters
        - 💾 Backup before delete
        """)
    
    with col2:
        st.markdown("""
        #### 🛡️ Safety:
        - ✅ Read-only by default
        - ✅ Manual approval option
        - ✅ Undo within 30 days
        - ✅ Encrypted connections
        - ✅ No data storage
        - ✅ Open source code
        - ✅ Privacy protected
        - ✅ GDPR compliant
        """)
    
    st.markdown("---")
    
    st.warning("""
    **⚠️ Important:** This is a demo app. To actually access and delete emails from your Gmail account, you need to:
    
    1. Set up Gmail API credentials from Google Cloud Console
    2. Install required packages: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`
    3. Implement OAuth2 authentication flow
    4. Use Gmail API methods to list, filter, and delete messages
    
    [📖 Gmail API Documentation](https://developers.google.com/gmail/api/reference/rest)
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 DASHBOARD", "🗑️ SPAM CLEANER", "📈 ANALYTICS", "⚙️ FILTERS"])
    
    # TAB 1: Dashboard
    with tab1:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        st.markdown('<div class="scanner"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Inbox Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.total_emails}</div>
                <div class="stat-label">Total Emails</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.spam_detected}</div>
                <div class="stat-label">Spam Detected</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.deleted}</div>
                <div class="stat-label">Deleted</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            clean_percent = ((st.session_state.total_emails - st.session_state.spam_detected) / st.session_state.total_emails * 100) if st.session_state.total_emails > 0 else 100
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{clean_percent:.1f}%</div>
                <div class="stat-label">Inbox Clean</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 SCAN FOR SPAM", use_container_width=True):
                with st.spinner("Scanning inbox..."):
                    progress = st.progress(0)
                    for i in range(100):
                        import time
                        time.sleep(0.01)
                        progress.progress(i + 1)
                    st.success(f"✅ Found {len(DEMO_SPAM)} spam emails!")
        
        with col2:
            if st.button("🗑️ DELETE ALL SPAM", use_container_width=True):
                st.session_state.deleted += st.session_state.spam_detected
                st.session_state.spam_detected = 0
                st.success(f"✅ Deleted {len(DEMO_SPAM)} spam emails!")
                st.rerun()
        
        with col3:
            if st.button("📥 EXPORT REPORT", use_container_width=True):
                st.info("📊 Report generated!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: Spam Cleaner
    with tab2:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 🗑️ Detected Spam Emails")
        
        if st.session_state.spam_detected == 0:
            st.success("✨ **Your inbox is clean!** No spam detected.")
        else:
            st.warning(f"⚠️ **{len(DEMO_SPAM)} spam emails** detected and ready for deletion")
            
            st.markdown("---")
            
            for idx, email in enumerate(DEMO_SPAM):
                st.markdown(f"""
                <div class="email-item">
                    <div class="email-subject">
                        {email['subject']}
                        <span class="spam-badge">SPAM {email['spam_score']}%</span>
                    </div>
                    <div class="email-sender">From: {email['sender']}</div>
                    <div class="email-date">{email['date']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col2:
                    if st.button(f"✅ Not Spam", key=f"keep_{idx}", use_container_width=True):
                        st.info(f"Kept: {email['subject'][:30]}...")
                with col3:
                    if st.button(f"🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                        st.success(f"Deleted: {email['subject'][:30]}...")
                
                if idx < len(DEMO_SPAM) - 1:
                    st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Analytics
    with tab3:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📈 Spam Analytics")
        
        # Create demo data
        df_stats = pd.DataFrame({
            'Category': ['Phishing', 'Marketing', 'Malware', 'Scam', 'Adult', 'Other'],
            'Count': [25, 45, 12, 18, 8, 15],
            'Percentage': [20, 37, 10, 15, 7, 12]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Spam by Category")
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🎯 Top Spam Senders")
            top_senders = pd.DataFrame({
                'Sender': ['lottery@fake-winner.com', 'pills@spam-mail.net', 'promo@scam-offers.biz'],
                'Spam Count': [45, 38, 32]
            })
            st.dataframe(top_senders, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### 📅 Spam Trend (Last 7 Days)")
        
        trend_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Spam Received': [12, 18, 15, 22, 19, 8, 6]
        })
        
        st.bar_chart(trend_data.set_index('Day'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 4: Filters
    with tab4:
        st.markdown('<div class="cyber-panel">', unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Custom Spam Filters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚫 Block Keywords")
            blocked_words = st.text_area(
                "Enter keywords (one per line):",
                value="viagra\ncasino\nfree money\nclick here\nurgent",
                height=150
            )
        
        with col2:
            st.markdown("#### 📧 Block Senders")
            blocked_senders = st.text_area(
                "Enter email addresses (one per line):",
                value="spam@example.com\nscam@fake.net",
                height=150
            )
        
        st.markdown("---")
        
        st.markdown("#### 🎯 Detection Rules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Block emails with excessive capitals", value=True)
            st.checkbox("Block emails with suspicious links", value=True)
            st.checkbox("Block emails from unknown senders", value=False)
        
        with col2:
            st.checkbox("Block emails with attachments from unknown", value=True)
            st.checkbox("Block emails with $$$$ symbols", value=True)
            st.checkbox("Block emails without unsubscribe link", value=False)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col2:
            if st.button("💾 SAVE FILTERS", type="primary", use_container_width=True):
                st.success("✅ Filters saved successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2.5rem; 
background: linear-gradient(135deg, rgba(0, 50, 25, 0.8) 0%, rgba(0, 30, 15, 0.8) 100%); 
border: 2px solid #00ff41;
border-radius: 20px; 
box-shadow: 0 0 40px rgba(0, 255, 65, 0.4);">
    <div style="font-size: 2.5rem; font-weight: 900; color: #00ff41; margin-bottom: 1rem; font-family: 'Orbitron', sans-serif; letter-spacing: 3px;">
        🛡️ GMAIL SPAM TERMINATOR
    </div>
    <div style="font-size: 1.3rem; color: #00ff88; font-weight: 700; margin-bottom: 0.5rem;">
        Made with ❤️ using Streamlit & Gmail API
    </div>
    <div style="font-size: 1.1rem; color: #00ffaa;">
        Secure • Fast • Efficient • AI-Powered
    </div>
    <div style="font-size: 0.95rem; margin-top: 1.5rem; color: #00ff88; font-weight: 600;">
        ⚡ Protect Your Inbox • Delete Spam Automatically • Stay Organized ⚡
    </div>
</div>
""", unsafe_allow_html=True)

