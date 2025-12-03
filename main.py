import streamlit as st
import pandas as pd
from datetime import datetime
import imaplib
import email
from email.header import decode_header
import json
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

# Page configuration
st.set_page_config(
    page_title="Gmail Spam Cleaner - Multiple Login Options",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0a0f0d 0%, #1a2f24 100%);
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #1a2e23 0%, #0f1e17 100%);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 255, 100, 0.2);
        border: 1px solid rgba(0, 255, 100, 0.2);
    }
    
    .login-box {
        background: linear-gradient(135deg, #234a38 0%, #1a3829 100%);
        border: 2px solid rgba(0, 255, 100, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem auto;
        box-shadow: 0 10px 40px rgba(0, 255, 100, 0.2);
    }
    
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
    }
    
    .user-email {
        font-size: 1.6rem;
        font-weight: 900;
        color: #000;
    }
    
    .live-badge {
        background: linear-gradient(135deg, #ff3366 0%, #ff1744 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 900;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 0, 1); }
    }
    
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
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        color: #000;
    }
    
    .stat-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0a4a2a;
        text-transform: uppercase;
    }
    
    .email-item {
        background: linear-gradient(135deg, #234a38 0%, #1a3829 100%);
        border-left: 5px solid #00ff64;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .email-item::before {
        content: '🔴 LIVE';
        position: absolute;
        top: 10px;
        right: 10px;
        background: #ff1744;
        color: white;
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
    }
    
    .email-meta {
        font-size: 0.95rem;
        color: #80ff9f;
    }
    
    .email-preview {
        font-size: 1rem;
        color: #99ffb3;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(0, 255, 100, 0.2);
        font-style: italic;
    }
    
    .spam-badge {
        background: linear-gradient(135deg, #ff3366 0%, #ff1744 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-left: 10px;
    }
    
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
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 255, 100, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0, 255, 100, 0.6);
    }
    
    .stTextInput input, .stTextInput input[type="password"] {
        background: rgba(30, 60, 45, 0.6) !important;
        border: 2px solid rgba(0, 255, 100, 0.3) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput label {
        color: #00ff64 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(30, 60, 45, 0.5);
        border-radius: 16px;
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 800;
        font-size: 1rem;
        color: #7fff9f;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff64 0%, #00cc50 100%) !important;
        color: #000 !important;
        box-shadow: 0 4px 16px rgba(0, 255, 100, 0.4);
    }
    
    .upload-box {
        border: 3px dashed rgba(0, 255, 100, 0.5);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(0, 255, 100, 0.05);
        transition: all 0.3s;
    }
    
    .upload-box:hover {
        border-color: #00ff64;
        background: rgba(0, 255, 100, 0.1);
    }
    
    h1, h2, h3 { color: #00ff64 !important; font-weight: 800 !important; }
    p, li { color: #b3ffcc !important; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = None
if 'connection_type' not in st.session_state:
    st.session_state.connection_type = None
if 'imap_conn' not in st.session_state:
    st.session_state.imap_conn = None
if 'gmail_service' not in st.session_state:
    st.session_state.gmail_service = None
if 'spam_emails' not in st.session_state:
    st.session_state.spam_emails = []
if 'deleted' not in st.session_state:
    st.session_state.deleted = 0

# Gmail API Functions
def authenticate_gmail_api(credentials_json):
    """Authenticate using uploaded credentials.json"""
    try:
        # Save uploaded file temporarily
        with open('temp_credentials.json', 'w') as f:
            f.write(credentials_json)
        
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'temp_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        # Clean up temp file
        if os.path.exists('temp_credentials.json'):
            os.remove('temp_credentials.json')
        
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        return None, str(e)

def get_user_profile_api(service):
    """Get user profile via API"""
    try:
        profile = service.users().getProfile(userId='me').execute()
        return profile['emailAddress']
    except:
        return None

def get_spam_emails_api(service, max_results=50):
    """Fetch spam via Gmail API"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:spam',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
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
                'preview': snippet,
                'size': message.get('sizeEstimate', 0),
                'is_real': True
            })
        
        return spam_emails
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def trash_email_api(service, email_id):
    """Trash email via API"""
    try:
        service.users().messages().trash(userId='me', id=email_id).execute()
        return True
    except:
        return False

# IMAP Functions
def connect_to_gmail_imap(email, password):
    """Connect via IMAP"""
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email, password)
        return imap, None
    except Exception as e:
        return None, str(e)

def get_spam_emails_imap(imap, max_emails=50):
    """Fetch spam via IMAP"""
    try:
        imap.select('"[Gmail]/Spam"')
        status, messages = imap.search(None, 'ALL')
        
        if status != 'OK':
            return []
        
        email_ids = messages[0].split()
        email_ids = email_ids[-max_emails:]
        spam_emails = []
        
        for email_id in email_ids:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            sender = msg.get('From', 'Unknown')
            date = msg.get('Date', 'Unknown')
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()[:300]
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode()[:300]
                except:
                    body = "Preview unavailable"
            
            spam_emails.append({
                'id': email_id.decode(),
                'subject': subject or 'No Subject',
                'sender': sender,
                'date': date,
                'preview': body or 'No preview',
                'is_real': True
            })
        
        return spam_emails
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def delete_email_imap(imap, email_id):
    """Delete via IMAP"""
    try:
        imap.select('"[Gmail]/Spam"')
        imap.store(email_id, '+FLAGS', '\\Deleted')
        imap.expunge()
        return True
    except:
        return False

# Main App
if not st.session_state.logged_in:
    # Login Page
    st.markdown('<h1 class="main-title">🛡️ Gmail Spam Cleaner Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose Your Login Method</p>', unsafe_allow_html=True)
    
    # Login method tabs
    tab1, tab2 = st.tabs(["📧 Email + Password Login", "📁 Upload JSON Credentials"])
    
    # TAB 1: Email/Password Login (IMAP)
    with tab1:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("### 🔐 Direct Login (IMAP)")
        
        st.info("""
        **Quick & Easy Login:**
        - No API setup needed
        - Just use App Password
        - Works immediately
        """)
        
        email_input = st.text_input("📧 Gmail Address", placeholder="your.email@gmail.com", key="imap_email")
        password_input = st.text_input("🔑 App Password", type="password", placeholder="16-character App Password", key="imap_pass")
        
        st.warning("""
        **⚠️ Use an App Password:**
        1. Go to [Google Account Security](https://myaccount.google.com/security)
        2. Enable 2-Step Verification
        3. Go to "App Passwords"
        4. Generate password for "Mail"
        5. Paste here (remove spaces)
        """)
        
        if st.button("🔓 LOGIN WITH IMAP", type="primary", use_container_width=True, key="imap_login"):
            if email_input and password_input:
                with st.spinner("🔐 Connecting to Gmail via IMAP..."):
                    imap, error = connect_to_gmail_imap(email_input, password_input)
                    
                    if imap:
                        st.session_state.logged_in = True
                        st.session_state.email = email_input
                        st.session_state.imap_conn = imap
                        st.session_state.connection_type = "IMAP"
                        st.success("✅ Connected via IMAP!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {error}")
            else:
                st.error("Please enter both email and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: JSON Upload (Gmail API)
    with tab2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("### 📁 Upload credentials.json")
        
        st.info("""
        **API Method (More Features):**
        - Full Gmail API access
        - More reliable
        - Advanced features
        """)
        
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "📤 Upload your credentials.json file",
            type=['json'],
            help="Download from Google Cloud Console"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            if st.button("🔗 CONNECT WITH API", type="primary", use_container_width=True, key="api_login"):
                with st.spinner("🔐 Authenticating with Gmail API..."):
                    # Read JSON content
                    credentials_content = uploaded_file.read().decode('utf-8')
                    
                    result = authenticate_gmail_api(credentials_content)
                    
                    if isinstance(result, tuple):
                        service, error = result
                        st.error(f"❌ Authentication failed: {error}")
                    else:
                        service = result
                        user_email = get_user_profile_api(service)
                        
                        if user_email:
                            st.session_state.logged_in = True
                            st.session_state.email = user_email
                            st.session_state.gmail_service = service
                            st.session_state.connection_type = "API"
                            st.success("✅ Connected via Gmail API!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Failed to get user profile")
        
        st.markdown("---")
        
        with st.expander("📖 How to get credentials.json"):
            st.markdown("""
            **Step-by-Step Guide:**
            
            1. **Go to Google Cloud Console**
               - Visit: https://console.cloud.google.com
            
            2. **Create a Project**
               - Click "Select Project" → "New Project"
               - Name it (e.g., "Gmail Cleaner")
            
            3. **Enable Gmail API**
               - Go to "APIs & Services" → "Library"
               - Search "Gmail API"
               - Click "Enable"
            
            4. **Create Credentials**
               - Go to "Credentials" → "Create Credentials"
               - Choose "OAuth 2.0 Client ID"
               - Application type: "Desktop app"
               - Download the JSON file
            
            5. **Upload Here**
               - Click the upload button above
               - Select your downloaded JSON file
               - Click "Connect with API"
            
            [📖 Official Documentation](https://developers.google.com/gmail/api/quickstart/python)
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Logged In - Show Dashboard
    
    # Connection type banner
    connection_badge = "🔴 LIVE - IMAP Connection" if st.session_state.connection_type == "IMAP" else "🔴 LIVE - Gmail API"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ff3366 0%, #ff1744 100%); 
    padding: 1rem 2rem; border-radius: 16px; margin-bottom: 2rem; 
    text-align: center; box-shadow: 0 4px 20px rgba(255, 0, 0, 0.4);
    animation: pulse 2s ease-in-out infinite;">
        <div style="font-size: 1.3rem; font-weight: 900; color: white;">
            {connection_badge}
        </div>
        <div style="font-size: 1rem; font-weight: 700; color: rgba(255,255,255,0.9); margin-top: 0.3rem;">
            Connected to YOUR Real Gmail Account - All Data is LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # User header
    st.markdown(f"""
    <div class="user-header">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div class="user-avatar">{st.session_state.email[0].upper()}</div>
            <div>
                <div class="user-email">{st.session_state.email}</div>
                <div style="color: #0a4a2a; font-weight: 700; margin-top: 0.3rem;">
                    ✅ Connected via {st.session_state.connection_type}
                </div>
            </div>
        </div>
        <div class="live-badge">🔴 LIVE DATA</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(st.session_state.spam_emails)}</div>
            <div class="stat-label">🚨 Spam Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_size = sum(email.get('size', 0) for email in st.session_state.spam_emails) / (1024 * 1024)
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{total_size:.1f} MB</div>
            <div class="stat-label">💾 Space Used</div>
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
        if st.button("🔌 LOGOUT", use_container_width=True):
            if st.session_state.imap_conn:
                st.session_state.imap_conn.logout()
            st.session_state.logged_in = False
            st.session_state.email = None
            st.session_state.imap_conn = None
            st.session_state.gmail_service = None
            st.session_state.spam_emails = []
            if os.path.exists('token.pickle'):
                os.remove('token.pickle')
            st.rerun()
    
    st.markdown("---")
    
    # Load spam button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        max_emails = st.slider("Number of emails to load:", 10, 100, 50)
    
    with col2:
        if st.button("🔍 LOAD SPAM", type="primary", use_container_width=True):
            with st.spinner("📡 Fetching YOUR spam emails..."):
                if st.session_state.connection_type == "IMAP":
                    st.session_state.spam_emails = get_spam_emails_imap(st.session_state.imap_conn, max_emails)
                else:
                    st.session_state.spam_emails = get_spam_emails_api(st.session_state.gmail_service, max_emails)
            
            if st.session_state.spam_emails:
                st.success(f"✅ Loaded {len(st.session_state.spam_emails)} REAL emails from YOUR Gmail!")
            else:
                st.info("🎉 No spam found in your inbox!")
    
    st.markdown("---")
    
    # Display emails
    if st.session_state.spam_emails:
        st.markdown(f"""
        <div style="font-size: 1.8rem; font-weight: 800; color: #00ff64; margin-bottom: 1.5rem;">
            🗑️ Your Spam Emails ({len(st.session_state.spam_emails)} found)
            <span style="font-size: 1rem; background: #ff1744; color: white; padding: 4px 12px; border-radius: 12px; margin-left: 10px;">
                🔴 REAL DATA FROM YOUR ACCOUNT
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, email_data in enumerate(st.session_state.spam_emails):
            st.markdown(f"""
            <div class="email-item">
                <div class="email-subject">
                    {email_data['subject']}
                    <span class="spam-badge">SPAM</span>
                </div>
                <div class="email-sender">📧 From: {email_data['sender']}</div>
                <div class="email-meta">🕒 {email_data['date']} | 📧 ID: {email_data['id'][:30]}...</div>
                <div class="email-preview">📝 {email_data['preview'][:200]}...</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col2:
                if st.button(f"👁️ Details", key=f"view_{idx}", use_container_width=True):
                    with st.expander("Full Email Details", expanded=True):
                        st.markdown(f"""
                        **🔴 REAL EMAIL FROM YOUR GMAIL**
                        
                        **Subject:** {email_data['subject']}  
                        **From:** {email_data['sender']}  
                        **Date:** {email_data['date']}  
                        **Message ID:** `{email_data['id']}`  
                        
                        **Preview:**  
                        {email_data['preview']}
                        """)
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                    success = False
                    if st.session_state.connection_type == "IMAP":
                        success = delete_email_imap(st.session_state.imap_conn, email_data['id'].encode())
                    else:
                        success = trash_email_api(st.session_state.gmail_service, email_data['id'])
                    
                    if success:
                        st.success("✅ Deleted!")
                        st.session_state.deleted += 1
                        st.session_state.spam_emails.pop(idx)
                        st.rerun()
            
            if idx < len(st.session_state.spam_emails) - 1:
                st.markdown("---")
    else:
        st.info("👆 Click 'LOAD SPAM' to fetch your real spam emails from Gmail")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: rgba(30, 60, 45, 0.4); 
border-radius: 16px; border: 1px solid rgba(0, 255, 100, 0.2);">
    <div style="font-size: 2rem; font-weight: 900; color: #00ff64;">
        🛡️ Gmail Spam Cleaner Pro
    </div>
    <div style="font-size: 1.1rem; color: #b3ffcc; margin-top: 0.5rem;">
        {"🔴 LIVE - " + st.session_state.connection_type + " - " + st.session_state.email if st.session_state.logged_in else "Choose Your Login Method"}
    </div>
    <div style="font-size: 0.9rem; color: #7fff9f; margin-top: 0.5rem;">
        Two Login Options • IMAP or Gmail API • Your Choice
    </div>
</div>
""", unsafe_allow_html=True)
