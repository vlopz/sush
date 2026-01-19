# 🔐 GitHub Authentication Streamlit App

A Streamlit app template with GitHub OAuth authentication.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## Features

- GitHub OAuth authentication
- Display authenticated user information
- Secure login/logout functionality

## Setup

### 1. Create a GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click on "OAuth Apps" > "New OAuth App"
3. Fill in the application details:
   - **Application name**: Your app name (e.g., "Sush Streamlit App")
   - **Homepage URL**: `http://localhost:8501` (for local development)
   - **Authorization callback URL**: `http://localhost:8501`
4. Click "Register application"
5. Copy the **Client ID**
6. Click "Generate a new client secret" and copy the **Client Secret**

### 2. Configure Environment Variables

Set the following environment variables with your GitHub OAuth credentials:

```bash
export GITHUB_CLIENT_ID="your_client_id_here"
export GITHUB_CLIENT_SECRET="your_client_secret_here"
export GITHUB_REDIRECT_URI="http://localhost:8501"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run streamlit_app.py
```

### 5. Authenticate

1. Open your browser to `http://localhost:8501`
2. Click the "Login with GitHub" link
3. Authorize the application on GitHub
4. You'll be redirected back to the app with your user information displayed

## How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
