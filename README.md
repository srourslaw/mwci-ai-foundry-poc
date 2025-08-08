# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Add your API keys to .streamlit/secrets.toml
# Replace with your actual API keys:
# OPENAI_API_KEY = "sk-your-openai-key-here"
# ANTHROPIC_API_KEY = "sk-ant-your-claude-key-here"

# Step 4: Test the application locally
streamlit run app.py

# Step 5: Push to GitHub
git add .
git commit -m " Initial commit: Manila Water AI Foundry POC"
git push -u origin main

# Step 6: Deploy to Streamlit Cloud
# 1. Go to https://share.streamlit.io/
# 2. Connect your GitHub repository
# 3. Add your API keys as secrets in the Streamlit Cloud dashboard
# 4. Deploy!

echo " Manila Water AI Foundry POC is ready!"
echo " Local URL: http://localhost:8501"
echo "☁️  Deploy to: https://share.streamlit.io/"