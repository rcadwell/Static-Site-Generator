# Run the static site generator #
python3 src/main.py

# Start the web server from the 'public' directory #
python3 -m http.server 8888 --directory public
