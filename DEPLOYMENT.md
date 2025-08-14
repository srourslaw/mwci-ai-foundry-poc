# 🚀 Deploy Manila Water AI Foundry to Streamlit Cloud

## Step-by-Step Deployment Guide

### 1. Your Code is Ready ✅
- ✅ Code pushed to: https://github.com/srourslaw/mwci-ai-foundry-poc
- ✅ Requirements.txt configured
- ✅ Main file: app.py
- ✅ All components working

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Click "New App"** 
4. **Fill in the details**:
   - Repository: `srourslaw/mwci-ai-foundry-poc`
   - Branch: `main`
   - Main file path: `app.py`
   - App name: `manila-water-ai-foundry` (or choose your own)

### 3. Configure API Keys (Two Options)

#### Option A: User Input (Recommended for Sharing)
- Users can add their own API keys directly in the dashboard sidebar
- Click "🤖 Configure AI Services" in the sidebar
- Add API keys and click "💾 Save API Keys"
- **Best for sharing publicly** - users bring their own keys!

#### Option B: Pre-configured Keys (Optional)
If you want to pre-configure keys, add these secrets in Streamlit Cloud settings:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
OPENAI_API_KEY = "your-openai-key-here"
ANTHROPIC_API_KEY = "your-claude-key-here"
```

### 4. Your Live URL
After deployment, your dashboard will be available at:
**https://manila-water-ai-foundry-YOUR-USERNAME.streamlit.app**

## Features That Will Work:
- ✅ Executive Dashboard with KPIs
- ✅ HR Assistant with AI responses (Gemini)
- ✅ Smart Ticketing with beautiful technician cards
- ✅ Chat with Data Analytics
- ✅ All visualizations and charts
- ✅ Mobile responsive design

## 🔥 Key Features:
- **Enhanced Technician Cards**: Beautiful status indicators and progress bars
- **AI-Powered**: Gemini integration for smart responses
- **Professional UI**: Manila Water branding throughout
- **Real-time Analytics**: Interactive charts and metrics

## Troubleshooting:
- If deployment fails, check the logs in Streamlit Cloud
- Make sure your API keys are added in the secrets section
- The app has fallback responses if API keys are missing

## 🎉 Ready to Share!
Once deployed, you can share your dashboard URL with anyone - it's completely public and professional!