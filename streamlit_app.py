import streamlit as st
import requests
import os

# GitHub OAuth Configuration
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
GITHUB_REDIRECT_URI = os.environ.get("GITHUB_REDIRECT_URI", "http://localhost:8501")

st.set_page_config(page_title="GitHub Auth Demo", page_icon="🔐")

st.title("🔐 GitHub Authentication Demo")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# Check for OAuth callback code in query parameters
query_params = st.query_params
if "code" in query_params and not st.session_state.authenticated:
    code = query_params["code"]
    
    # Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"
    token_data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI
    }
    headers = {"Accept": "application/json"}
    
    try:
        token_response = requests.post(token_url, data=token_data, headers=headers)
        token_json = token_response.json()
        
        if "access_token" in token_json:
            access_token = token_json["access_token"]
            
            # Get user info from GitHub
            user_url = "https://api.github.com/user"
            user_headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/json"
            }
            user_response = requests.get(user_url, headers=user_headers)
            user_data = user_response.json()
            
            st.session_state.authenticated = True
            st.session_state.user_info = user_data
            st.session_state.access_token = access_token
            
            # Clear the code from URL
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")

# Display content based on authentication status
if st.session_state.authenticated and st.session_state.user_info:
    st.success("✅ Successfully authenticated with GitHub!")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.user_info.get("avatar_url"):
            st.image(st.session_state.user_info["avatar_url"], width=100)
    with col2:
        st.write(f"**Name:** {st.session_state.user_info.get('name', 'N/A')}")
        st.write(f"**Username:** {st.session_state.user_info.get('login', 'N/A')}")
        st.write(f"**Email:** {st.session_state.user_info.get('email', 'Not public')}")
        st.write(f"**Bio:** {st.session_state.user_info.get('bio', 'N/A')}")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.access_token = None
        st.rerun()
else:
    st.write("Please authenticate with GitHub to continue.")
    
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        st.warning("⚠️ GitHub OAuth credentials not configured. Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables.")
        
        with st.expander("How to set up GitHub OAuth"):
            st.markdown("""
            1. Go to GitHub Settings > Developer settings > OAuth Apps
            2. Click "New OAuth App"
            3. Fill in the application details:
               - Application name: Your app name
               - Homepage URL: http://localhost:8501
               - Authorization callback URL: http://localhost:8501
            4. After creating the app, copy the Client ID and generate a Client Secret
            5. Set environment variables:
               ```bash
               export GITHUB_CLIENT_ID="your_client_id"
               export GITHUB_CLIENT_SECRET="your_client_secret"
               export GITHUB_REDIRECT_URI="http://localhost:8501"
               ```
            6. Restart the Streamlit app
            """)
    else:
        # Generate GitHub OAuth URL
        github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email"
        
        st.markdown(f"[🔗 Login with GitHub]({github_auth_url})", unsafe_allow_html=True)
        st.info("Click the link above to authenticate with GitHub")
