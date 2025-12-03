import streamlit as st
import random
import string
from datetime import datetime, timedelta
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Cleaner Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CLEAN & SIMPLE CSS with perfect visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean gradient background */
    .stApp {
        background: linear-gradient(135deg, #0a0f0d 0%, #1a2f24 100%);
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #1a2e23 0%, #0f1e17 100%);
        border-radius: 24px;
        padding: 2rem;
        max-width: 1400px;
        box-shadow: 0 8px 32px rgba(0, 255, 100, 0.2);
        border: 1px solid rgba(0, 255, 100, 0.2);
    }
    
    /* User account header */
    .user-header {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 255, 100, 0.3);
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 900;
        color: #00cc50;
        margin-right: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .user-info {
        flex: 1;
    }
    
    .user-email {
        font-size: 1.5rem;
        font-weight: 800;
        color: #000;
        margin: 0;
    }
    
    .user-status {
        font-size: 1rem;
        font-weight: 600;
        color: #0a4a2a;
        margin: 0.3rem 0 0 0;
    }
    
    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00ff64;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(0, 255, 100, 0.6);
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        color: #7fff9f;
        margin-bottom: 2rem;
    }
    
    /* Stats boxes - HIGH CONTRAST */
    .stat-box {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 255, 100, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 255, 100, 0.5);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        color: #000;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0a4a2a;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Section panels */
    .section-panel {
        background: rgba(30, 60, 45, 0.6);
        border: 2px solid rgba(0, 255, 100, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00ff64;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    /* Email items - MUCH BETTER CONTRAST */
    .email-item {
        background: linear-gradient(135deg, #234a38 0%, #1a3829 100%);
        border-left: 5px solid #00ff64;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .email-item:hover {
        border-left-width: 8px;
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(0, 255, 100, 0.3);
    }
    
    .email-subject {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
    }
    
    .email-sender {
        font-size: 1.1rem;
        font-weight: 600;
        color: #b3ffcc;
        margin-bottom: 0.5rem;
    }
    
    .email-meta {
        font-size: 0.95rem;
        font-weight: 500;
        color: #80ff9f;
        opacity: 0.9;
    }
    
    .email-preview {
        font-size: 1rem;
        font-weight: 500;
        color: #99ffb3;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(0, 255, 100, 0.2);
        font-style: italic;
    }
    
    /* Badges */
    .spam-badge {
        background: linear-gradient(135deg, #ff3366 0%, #ff1744 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin-left: 10px;
        box-shadow: 0 2px 12px rgba(255, 0, 0, 0.4);
    }
    
    .category-badge {
        background: rgba(255, 165, 0, 0.9);
        color: #000;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin: 0 4px;
    }
    
    /* Buttons - HIGH CONTRAST */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%);
        color: #000;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 255, 100, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0, 255, 100, 0.6);
        background: linear-gradient(135deg, #00ff88 0%, #00dd64 100%);
    }
    
    /* Tabs - CLEAR & VISIBLE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(30, 60, 45, 0.5);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 100, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 800;
        font-size: 1rem;
        color: #7fff9f;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 100, 0.1);
        color: #00ff64;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%) !important;
        color: #000 !important;
        box-shadow: 0 4px 16px rgba(0, 255, 100, 0.4);
    }
    
    /* Metrics - BOLD & VISIBLE */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 900;
        color: #00ff64 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 700;
        color: #b3ffcc !important;
        text-transform: uppercase;
    }
    
    /* Alerts - HIGH VISIBILITY */
    .stSuccess {
        background: rgba(0, 255, 100, 0.15) !important;
        border: 2px solid #00ff64 !important;
        border-radius: 12px !important;
        color: #00ff64 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.15) !important;
        border: 2px solid #ffaa00 !important;
        border-radius: 12px !important;
        color: #ffcc00 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    .stInfo {
        background: rgba(0, 200, 255, 0.15) !important;
        border: 2px solid #00ccff !important;
        border-radius: 12px !important;
        color: #66ddff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Form inputs */
    .stSelectbox > div > div,
    .stTextArea textarea,
    .stTextInput input {
        background: rgba(30, 60, 45, 0.6) !important;
        border: 2px solid rgba(0, 255, 100, 0.3) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Headers - BRIGHT & CLEAR */
    h1, h2, h3, h4 {
        color: #00ff64 !important;
        font-weight: 800 !important;
    }
    
    /* Text - READABLE */
    p, li, span, label {
        color: #b3ffcc !important;
        font-weight: 500 !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border: 2px solid rgba(0, 255, 100, 0.3);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff64 0%, #00cc50 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'total_emails' not in st.session_state:
    st.session_state.total_emails = 0
if 'spam_detected' not in st.session_state:
    st.session_state.spam_detected = 0
if 'deleted' not in st.session_state:
    st.session_state.deleted = 0
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0

# Demo spam emails (simplified)
DEMO_SPAM = [
    {
        "subject": "🎁 WINNER: You've won $1,000,000!",
        "sender": "lottery@fake-winner.com",
        "date": "2 hours ago",
        "spam_score": 98,
        "category": "Scam",
        "preview": "Congratulations! You are the lucky winner of our international lottery draw..."
    },
    {
        "subject": "URGENT: Your account will be suspended",
        "sender": "security@fake-paypal.com",
        "date": "3 hours ago",
        "spam_score": 96,
        "category": "Phishing",
        "preview": "Suspicious activity detected on your account. Verify immediately or lose access..."
    },
    {
        "subject": "🔥 Meet singles in your area NOW",
        "sender": "dating@spam-central.org",
        "date": "5 hours ago",
        "spam_score": 97,
        "category": "Adult",
        "preview": "Thousands of singles waiting to meet you tonight. Sign up now for free..."
    },
    {
        "subject": "FREE iPhone 15 Pro - Limited Time!",
        "sender": "promo@scam-offers.biz",
        "date": "1 day ago",
        "spam_score": 95,
        "category": "Phishing",
        "preview": "You've been selected to receive a free iPhone 15. Click here to claim now..."
    },
    {
        "subject": "💰 Work from home - Earn $5000/week",
        "sender": "jobs@mlm-scam.info",
        "date": "1 day ago",
        "spam_score": 94,
        "category": "Scam",
        "preview": "No experience needed! Start earning today with our proven system..."
    },
    {
        "subject": "Re: Invoice #12345 [VIRUS DETECTED]",
        "sender": "billing@malware-sender.tk",
        "date": "2 days ago",
        "spam_score": 100,
        "category": "Malware",
        "preview": "Please see attached invoice. Download and open the PDF to view payment details..."
    },
]

# Sidebar - Simplified
with st.sidebar:
    st.markdown("### 🔐 Gmail Login")
    
    if not st.session_state.connected:
        user_email_input = st.text_input("📧 Email Address", placeholder="your.email@gmail.com")
        
        if st.button("🔗 CONNECT", type="primary", use_container_width=True):
            if user_email_input:
                with st.spinner("Connecting..."):
                    import time
                    time.sleep(1.5)
                    st.session_state.connected = True
                    st.session_state.user_email = user_email_input
                    st.session_state.total_emails = random.randint(500, 1500)
                    st.session_state.spam_detected = len(DEMO_SPAM)
                    st.success("✅ Connected!")
                    st.balloons()
                    st.rerun()
            else:
                st.error("Please enter your email")
    else:
        st.success(f"✅ Connected as:")
        st.info(f"**{st.session_state.user_email}**")
        
        st.markdown("---")
        st.metric("🔍 Total Scans", st.session_state.scan_count)
        st.metric("🗑️ Emails Deleted", st.session_state.deleted)
        
        st.markdown("---")
        
        if st.button("🔌 DISCONNECT", use_container_width=True):
            st.session_state.connected = False
            st.session_state.user_email = None
            st.rerun()

# Main content
if not st.session_state.connected:
    # Landing page
    st.markdown('<h1 class="main-title">🛡️ Gmail Spam Cleaner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Email Protection System</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🤖 **Smart AI Detection** - 99.8% accuracy
        - 🗑️ **Auto-Delete Spam** - Set it and forget it
        - 📊 **Real-Time Stats** - Monitor your inbox
        - 🔒 **100% Secure** - Bank-grade encryption
        - ⚡ **Lightning Fast** - Process 1000s of emails
        - 💾 **Backup System** - Recover if needed
        """)
    
    with col2:
        st.markdown("### 🛡️ Security")
        st.markdown("""
        - ✅ **OAuth2 Login** - Secure authentication
        - ✅ **Read-Only Mode** - Safe by default
        - ✅ **No Data Storage** - Privacy first
        - ✅ **30-Day Undo** - Recover deleted emails
        - ✅ **Open Source** - Transparent code
        - ✅ **GDPR Compliant** - Legal protection
        """)
    
    st.markdown("---")
    
    st.info("""
    **📝 To use this app:**
    
    1. Enter your Gmail address in the sidebar
    2. Click "CONNECT" to authorize
    3. Start scanning and cleaning spam!
    
    **Note:** This is a demo. Real Gmail integration requires API setup.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Show user header
    st.markdown(f"""
    <div class="user-header">
        <div class="user-avatar">{st.session_state.user_email[0].upper()}</div>
        <div class="user-info">
            <div class="user-email">{st.session_state.user_email}</div>
            <div class="user-status">✅ Connected & Protected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🛡️ Spam Cleaner Dashboard</h1>', unsafe_allow_html=True)
    
    # Stats
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
            <div class="stat-label">🚨 Spam Found</div>
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
        clean_rate = ((st.session_state.total_emails - st.session_state.spam_detected) / st.session_state.total_emails * 100) if st.session_state.total_emails > 0 else 100
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{clean_rate:.0f}%</div>
            <div class="stat-label">✨ Clean</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 SCAN INBOX", use_container_width=True):
            with st.spinner("Scanning..."):
                progress = st.progress(0)
                for i in range(100):
                    import time
                    time.sleep(0.015)
                    progress.progress(i + 1)
                st.session_state.scan_count += 1
                st.success(f"✅ Found {len(DEMO_SPAM)} spam emails!")
    
    with col2:
        if st.button("🗑️ DELETE ALL SPAM", use_container_width=True):
            if st.session_state.spam_detected > 0:
                st.session_state.deleted += st.session_state.spam_detected
                st.session_state.spam_detected = 0
                st.success("✅ All spam deleted!")
                st.rerun()
            else:
                st.info("No spam to delete")
    
    with col3:
        if st.button("📥 EXPORT REPORT", use_container_width=True):
            df = pd.DataFrame(DEMO_SPAM)
            st.download_button(
                "Download CSV",
                df.to_csv(index=False),
                "spam_report.csv",
                "text/csv"
            )
    
    with col4:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Spam list
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">🚨 Spam Emails ({len(DEMO_SPAM)} found)</div>', unsafe_allow_html=True)
    
    if st.session_state.spam_detected == 0:
        st.success("✨ Your inbox is clean! No spam detected.")
    else:
        for idx, email in enumerate(DEMO_SPAM):
            st.markdown(f"""
            <div class="email-item">
                <div class="email-subject">
                    {email['subject']}
                    <span class="spam-badge">SPAM {email['spam_score']}%</span>
                    <span class="category-badge">{email['category']}</span>
                </div>
                <div class="email-sender">📧 From: {email['sender']}</div>
                <div class="email-meta">🕒 {email['date']}</div>
                <div class="email-preview">📝 {email['preview']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col2:
                if st.button(f"✅ Keep", key=f"keep_{idx}", use_container_width=True):
                    st.info("Moved to inbox")
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                    st.session_state.deleted += 1
                    st.success("Deleted!")
            
            if idx < len(DEMO_SPAM) - 1:
                st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(30, 60, 45, 0.4); 
border-radius: 16px; border: 1px solid rgba(0, 255, 100, 0.2);">
    <div style="font-size: 2rem; font-weight: 900; color: #00ff64; margin-bottom: 0.5rem;">
        🛡️ Gmail Spam Cleaner Pro
    </div>
    <div style="font-size: 1.1rem; color: #b3ffcc; font-weight: 600;">
        Made with ❤️ using Streamlit | Secure • Fast • Effective
    </div>
</div>
""", unsafe_allow_html=True)
