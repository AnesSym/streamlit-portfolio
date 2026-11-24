mkdir -p ~/.streamlit/

# Server settings only; the theme lives in the project's .streamlit/config.toml
cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
port = $PORT
EOF
