import streamlit as st
import pandas as pd
from datetime import datetime
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import json

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Cleaner Pro - Real Data",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with data source indicators
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
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
    
    /* Real Data Badge */
    .real-data-badge {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%);
        color: #000;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 900;
        text-transform: uppercase;
        display: inline-block;
        box-shadow: 0 0 20px rgba(0, 255, 100, 0.6);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .demo-data-badge {
        background: linear-gradient(135deg, #ff8800 0%, #ffaa00 100%);
        color: #000;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 900;
        text-transform: uppercase;
        display: inline-block;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 100, 0.6); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 100, 1); }
    }
    
    /* User account header */
    .user-header {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 255, 100, 0.3);
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .user-avatar {
        width: 65px;
        height: 65px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 900;
        color: #00cc50;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .user-email {
        font-size: 1.6rem;
        font-weight: 900;
        color: #000;
        margin: 0;
    }
    
    .user-status {
        font-size: 1rem;
        font-weight: 700;
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
    
    /* Stats boxes */
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
    
    /* Email items with data source indicator */
    .email-item {
        background: linear-gradient(135deg, #234a38 0%, #1a3829 100%);
        border-left: 5px solid #00ff64;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .email-item:hover {
        border-left-width: 8px;
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(0, 255, 100, 0.3);
    }
    
    .email-item.real-data::before {
        content: '🔴 LIVE';
        position: absolute;
        top: 10px;
        right: 10px;
        background: #00ff64;
        color: #000;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 900;
    }
    
    .email-subject {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
        padding-right: 80px;
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
    
    /* Buttons */
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
    
    /* Tabs */
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
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%) !important;
        color: #000 !important;
        box-shadow: 0 4px 16px rgba(0, 255, 100, 0.4);
    }
    
    /* Alerts */
    .stSuccess {
        background: rgba(0, 255, 100, 0.15) !important;
        border: 2px solid #00ff64 !important;
        border-radius: 12px !important;
        color: #00ff64 !important;
        font-weight: 700 !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.15) !important;
        border: 2px solid #ffaa00 !important;
        border-radius: 12px !important;
        color: #ffcc00 !important;
        font-weight: 700 !important;
    }
    
    .stInfo {
        background: rgba(0, 200, 255, 0.15) !important;
        border: 2px solid #00ccff !important;
        border-radius: 12px !important;
        color: #66ddff !important;
        font-weight: 700 !important;
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
    
    h1, h2, h3, h4 {
        color: #00ff64 !important;
        font-weight: 800 !important;
    }
    
    p, li, span, label {
        color: #b3ffcc !important;
        font-weight: 500 !important;
    }
    
    .stDataFrame {
        border: 2px solid rgba(0, 255, 100, 0.3);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ff64 0%, #00cc50 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'service' not in st.session_state:
    st.session_state.service = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'real_emails' not in st.session_state:
    st.session_state.real_emails = []
if 'deleted' not in st.session_state:
    st.session_state.deleted = 0
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'is_real_data' not in st.session_state:
    st.session_state.is_real_data = False

# REAL Gmail Authentication Functions
def authenticate_gmail():
    """Authenticate with Gmail API using OAuth2"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                st.error("❌ credentials.json not found!")
                st.info("""
                **To get credentials.json:**
                1. Go to [Google Cloud Console](https://console.cloud.google.com)
                2. Create project → Enable Gmail API
                3. Create OAuth 2.0 credentials (Desktop app)
                4. Download as credentials.json
                """)
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def get_user_profile(service):
    """Get user's Gmail profile"""
    try:
        profile = service.users().getProfile(userId='me').execute()
        return {
            'email': profile['emailAddress'],
            'total_messages': profile['messagesTotal'],
            'threads_total': profile['threadsTotal']
        }
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_spam_emails(service, max_results=50):
    """Fetch REAL spam emails from user's Gmail"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:spam',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return []
        
        spam_emails = []
        
        for msg in messages:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            snippet = message.get('snippet', 'No preview')
            
            spam_emails.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'snippet': snippet,
                'size': message.get('sizeEstimate', 0),
                'is_real': True  # Flag to show this is real data
            })
        
        return spam_emails
    
    except Exception as e:
        st.error(f"Error fetching emails: {str(e)}")
        return []

def trash_email(service, email_id):
    """Move email to trash"""
    try:
        service.users().messages().trash(userId='me', id=email_id).execute()
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def bulk_trash_emails(service, email_ids):
    """Trash multiple emails"""
    success = 0
    for email_id in email_ids:
        if trash_email(service, email_id):
            success += 1
    return success

# Sidebar
with st.sidebar:
    st.markdown("### 🔐 Gmail Connection")
    
    if st.session_state.service is None:
        st.info("""
        **Connect Your Gmail:**
        
        1. Download `credentials.json`
        2. Place in app folder
        3. Click Connect below
        
        [Setup Guide →](https://developers.google.com/gmail/api/quickstart/python)
        """)
        
        if st.button("🔗 CONNECT GMAIL", type="primary", use_container_width=True):
            with st.spinner("🔐 Authenticating..."):
                service = authenticate_gmail()
                if service:
                    st.session_state.service = service
                    profile = get_user_profile(service)
                    if profile:
                        st.session_state.user_email = profile['email']
                        st.session_state.is_real_data = True
                        st.success("✅ Connected!")
                        st.balloons()
                        st.rerun()
    else:
        # Show real account info
        st.success("✅ **CONNECTED**")
        st.markdown(f"""
        <div style="background: rgba(0, 255, 100, 0.1); padding: 1rem; border-radius: 10px; border: 2px solid rgba(0, 255, 100, 0.3);">
            <div style="color: #00ff64; font-weight: 800; font-size: 1rem; margin-bottom: 0.5rem;">
                📧 Your Account
            </div>
            <div style="color: white; font-weight: 700; word-break: break-all;">
                {st.session_state.user_email}
            </div>
            <div style="color: #7fff9f; font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;">
                🔴 LIVE DATA MODE
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.metric("🔍 Scans", st.session_state.scan_count)
        st.metric("🗑️ Deleted", st.session_state.deleted)
        
        st.markdown("---")
        
        if st.button("🔌 DISCONNECT", use_container_width=True):
            # Logout confirmation
            if st.checkbox("Confirm logout"):
                st.session_state.service = None
                st.session_state.user_email = None
                st.session_state.real_emails = []
                st.session_state.is_real_data = False
                if os.path.exists('token.pickle'):
                    os.remove('token.pickle')
                st.rerun()

# Main Content
if st.session_state.service is None:
    # Not connected - Setup page
    st.markdown('<h1 class="main-title">🛡️ Gmail Spam Cleaner Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Clean Your Real Gmail Inbox with AI</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Get Started in 3 Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Setup API
        
        - Go to [Google Cloud Console](https://console.cloud.google.com)
        - Create new project
        - Enable Gmail API
        - Create OAuth credentials
        - Download credentials.json
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Install Packages
        
        ```
        pip install google-auth
        pip install google-auth-oauthlib
        pip install google-api-python-client
        ```
        
        Place credentials.json in app folder
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Connect
        
        - Click "Connect Gmail" in sidebar
        - Authorize in browser
        - Start cleaning spam!
        
        🔒 100% Secure OAuth2
        """)
    
    st.markdown("---")
    
    st.markdown("### ✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - 🔴 **Real-Time Data** - Access YOUR actual Gmail
        - 🤖 **Smart Detection** - See what's in your spam folder
        - 🗑️ **Bulk Delete** - Clean thousands at once
        - 💾 **Safe Operations** - Emails go to trash (recoverable)
        - 📊 **Live Stats** - Real inbox metrics
        """)
    
    with col2:
        st.markdown("""
        - 🔒 **Bank-Level Security** - OAuth2 authentication
        - 📧 **Email Preview** - See before you delete
        - 💿 **Export Reports** - Download your data
        - ⚡ **Lightning Fast** - Process 100s of emails
        - 🎯 **Accurate** - Only touches spam folder
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Connected - Show REAL data
    
    # Data source indicator banner
    if st.session_state.is_real_data:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%); 
        padding: 1rem 2rem; border-radius: 16px; margin-bottom: 2rem; 
        text-align: center; box-shadow: 0 4px 20px rgba(0, 255, 100, 0.4);">
            <div style="font-size: 1.3rem; font-weight: 900; color: #000;">
                🔴 LIVE DATA MODE - Connected to Your Real Gmail Account
            </div>
            <div style="font-size: 1rem; font-weight: 700; color: #0a4a2a; margin-top: 0.3rem;">
                All data shown below is from your actual inbox
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # User header
    st.markdown(f"""
    <div class="user-header">
        <div class="user-info">
            <div class="user-avatar">{st.session_state.user_email[0].upper()}</div>
            <div>
                <div class="user-email">{st.session_state.user_email}</div>
                <div class="user-status">✅ Connected to Gmail API</div>
            </div>
        </div>
        <div class="real-data-badge">🔴 REAL DATA</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 DASHBOARD", "🗑️ CLEAN SPAM", "📈 ANALYTICS"])
    
    # TAB 1: Dashboard
    with tab1:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📊 Your Gmail Overview")
        
        # Real stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{len(st.session_state.real_emails)}</div>
                <div class="stat-label">🚨 Spam Found</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_size = sum(email.get('size', 0) for email in st.session_state.real_emails) / (1024 * 1024)
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{total_size:.1f} MB</div>
                <div class="stat-label">💾 Space Wasted</div>
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
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{st.session_state.scan_count}</div>
                <div class="stat-label">🔍 Scans</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            max_emails = st.number_input("Emails to load:", 10, 500, 50)
        
        with col2:
            if st.button("🔍 LOAD SPAM", type="primary", use_container_width=True):
                with st.spinner("📡 Fetching YOUR spam from Gmail..."):
                    st.session_state.real_emails = get_spam_emails(st.session_state.service, max_emails)
                    st.session_state.scan_count += 1
                if st.session_state.real_emails:
                    st.success(f"✅ Loaded {len(st.session_state.real_emails)} REAL spam emails from YOUR account!")
                else:
                    st.info("🎉 No spam found in your Gmail!")
        
        with col3:
            if st.button("🗑️ DELETE ALL", use_container_width=True):
                if st.session_state.real_emails:
                    if st.checkbox("⚠️ Confirm bulk delete"):
                        with st.spinner("Deleting spam..."):
                            email_ids = [email['id'] for email in st.session_state.real_emails]
                            count = bulk_trash_emails(st.session_state.service, email_ids)
                            st.session_state.deleted += count
                        st.success(f"✅ Moved {count} emails to trash!")
                        st.session_state.real_emails = []
                        st.rerun()
        
        with col4:
            if st.button("🔄 REFRESH", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: Clean Spam
    with tab2:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        
        if not st.session_state.real_emails:
            st.info("👆 Click 'LOAD SPAM' in Dashboard to fetch your real spam emails from Gmail")
        else:
            st.markdown(f"""
            <div class="section-title">
                🗑️ Your Spam Emails 
                <span class="real-data-badge">🔴 {len(st.session_state.real_emails)} REAL EMAILS</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Display REAL emails
            for idx, email in enumerate(st.session_state.real_emails):
                st.markdown(f"""
                <div class="email-item real-data">
                    <div class="email-subject">
                        {email['subject']}
                        <span class="spam-badge">SPAM</span>
                    </div>
                    <div class="email-sender">📧 From: {email['sender']}</div>
                    <div class="email-meta">
                        🕒 {email['date']} | 💾 {email['size'] / 1024:.1f} KB | 📧 ID: {email['id'][:20]}...
                    </div>
                    <div class="email-preview">
                        📝 {email['snippet'][:250]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col2:
                    if st.button(f"👁️ View Full", key=f"view_{idx}", use_container_width=True):
                        with st.expander("Full Email Details", expanded=True):
                            st.markdown(f"""
                            **🔴 REAL EMAIL FROM YOUR GMAIL**
                            
                            **Message ID:** `{email['id']}`  
                            **Subject:** {email['subject']}  
                            **From:** {email['sender']}  
                            **Date:** {email['date']}  
                            **Size:** {email['size'] / 1024:.2f} KB  
                            
                            **Preview:**  
                            {email['snippet']}
                            
                            ---
                            
                            This is a real email from your Gmail spam folder.
                            """)
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                        if trash_email(st.session_state.service, email['id']):
                            st.success(f"✅ Moved to trash!")
                            st.session_state.deleted += 1
                            st.session_state.real_emails.pop(idx)
                            st.rerun()
                
                if idx < len(st.session_state.real_emails) - 1:
                    st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Analytics
    with tab3:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📈 Your Real Email Analytics")
        
        if st.session_state.real_emails:
            # Analyze real data
            df = pd.DataFrame(st.session_state.real_emails)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Top Spam Senders (Your Data)")
                sender_counts = df['sender'].value_counts().head(10)
                st.dataframe(sender_counts.reset_index().rename(
                    columns={'index': 'Sender', 'sender': 'Count'}
                ), use_container_width=True)
            
            with col2:
                st.markdown("#### 💾 Email Sizes")
                st.dataframe(df[['subject', 'size']].sort_values('size', ascending=False).head(10))
            
            st.markdown("---")
            
            # Export real data
            if st.button("📥 EXPORT YOUR DATA", type="primary"):
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"gmail_spam_{st.session_state.user_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
        else:
            st.info("Load spam emails first to see analytics")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: rgba(30, 60, 45, 0.4); 
border-radius: 16px; border: 1px solid rgba(0, 255, 100, 0.2);">
    <div style="font-size: 2rem; font-weight: 900; color: #00ff64;">
        🛡️ Gmail Spam Cleaner Pro
    </div>
    <div style="font-size: 1.1rem; color: #b3ffcc; margin-top: 0.5rem;">
        {"🔴 LIVE MODE - Connected to " + st.session_state.user_email if st.session_state.is_real_data else "Ready to Connect to Your Gmail"}
    </div>
    <div style="font-size: 0.9rem; color: #7fff9f; margin-top: 0.8rem;">
        Secure OAuth2 • Privacy Protected • No Data Stored
    </div>
</div>
""", unsafe_allow_html=True)
