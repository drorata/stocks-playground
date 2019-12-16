# Taken from:
# https://github.com/MaartenGr/streamlit_guide/blob/336c38aa72b3b4cc5f0aed98b561b6a37b3155c3/setup.sh

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" >~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" >~/.streamlit/config.toml
