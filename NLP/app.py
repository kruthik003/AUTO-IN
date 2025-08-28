# # app.py

# from flask import Flask, render_template
# import subprocess
# import threading

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def run_process():
#     subprocess.call(['python', 'main.py'])

# def run_display():
#     subprocess.call(['python', 'display.py'])

# @app.route('/run_both')
# def run_both():
#     # Start both process and display in separate threads
#     process_thread = threading.Thread(target=run_process)
#     display_thread = threading.Thread(target=run_display)
#     process_thread.start()
#     display_thread.start()
#     return 'Process and Display started successfully.'

# if __name__ == '__main__':
#     app.run(debug=True)
