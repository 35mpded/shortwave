# Importing necessary libraries: Flask for web server, otpyf for one-time pad operations, configparser for parsing the config.ini file and so on.
from flask import Flask, request, render_template, send_from_directory
import otpyf
import configparser

# Initialize the configparser and read settings from the 'config.ini'
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve the settings from the config file
checkerboard = config['DEFAULT']['checkerboard']
pads_recv = config['DEFAULT']['pads_recv']
pad_send = config['DEFAULT']['pad_send']
cipher_length = int(config['DEFAULT']['cipher_length'])
num_pads = int(config['DEFAULT']['num_pads'])
numbers = config['DEFAULT']['numbers']
alpha = config['DEFAULT']['alpha']
prepend_audio = config['DEFAULT']['prepend_audio']
prepend_audio = config['DEFAULT']['prepend_audio']
append_audio = config['DEFAULT']['append_audio']

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the index page. Handle GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables to store various encryption/decryption or status related information
    enc_plaintext = ''
    enc_plaincode = ''
    enc_ciphertext = ''
    enc_otp_key = ''
    enc_otp_key_id = ''
    dec_plaintext = ''
    dec_plaincode = ''
    dec_ciphertext = ''
    dec_otp_key = ''
    dec_otp_key_id = ''
    status = ''
    # Handle the POST (form submittion) request.
    if request.method == 'POST':
        # Use `user_input` as the message to be encrypted
        user_input = request.form['input_text']
        # Handle encryption
        if 'encrypt' in request.form:
            # Store the user input from the textbox
            plaintext = user_input  
            # Check if the user entered any message for encryption
            if user_input:
                # Load the checkerboard from the CSV file specified in the config.ini
                checkerboard_manual = otpyf.csv_checkerboard_to_dict(checkerboard)
                # Encode the message to plaincode
                plaincode = otpyf.straddle(plaintext, checkerboard_manual, checkerboard_manual['F/L'], cipher_length)
                # Split the encoded message (plaincode) into groups of five digits and send it to the HTML form
                enc_plaincode = otpyf.split_into_groups_of_five(plaincode)
                # Decode the encoded message and send it to the HTML form
                enc_plaintext = otpyf.unstraddle(plaincode, checkerboard_manual, checkerboard_manual['F/L'])
                # Run the encryption procedure in a try block to catch any errors such as unavailable and/or malformatted encryption pad (key) or file.
                try:
                    # Encrypt the plaincode by using a random key from the jsonl file specified in the config.ini
                    cipher, otp_key, otp_key_id = otpyf.encrypt_init(pad_send, plaincode, cipher_length)
                    # Send the encryption one-time pad key ID to the HTML form
                    enc_otp_key_id = otp_key_id
                    # Send the encryption one-time pad key to the HTML form
                    enc_otp_key = otpyf.split_into_groups_of_five(otp_key)
                    # Split the ciphertext into groups of five digits and send it to the HTML
                    enc_ciphertext = otpyf.split_into_groups_of_five(cipher)
                # Catch any errors
                except Exception as e:
                    # Send any errors to the HTML form
                    status = e
            else:
                # Do nothing if the user did not provide a message for encryption. User will be notified via the HTML form.
                status = "Enter the message for encryption..."
        # Handle decryption
        elif 'decrypt' in request.form:
            # Store the user input from the textbox and remove any whitespace characters
            ciphertext = user_input.replace(" ", "")
            # Check if the user entered a message for decryption
            if ciphertext:
                # Load the checkerboard from the CSV file specified in the config.ini
                checkerboard_manual = otpyf.csv_checkerboard_to_dict(checkerboard)
                # Run the decryption procedure in a try block to catch any errors such as unavailable and/or malformatted encryption pad (key) or file.
                try:
                    # Decrypt the ciphertext to plaincode
                    plaincode, otp_key, otp_key_id = otpyf.decrypt_init(pads_recv, ciphertext)
                    # Send the decryption one-time pad key ID to the HTML form
                    dec_otp_key_id = otp_key_id
                    # Send the decryption one-time pad key to the HTML form
                    dec_otp_key = otpyf.split_into_groups_of_five(otp_key)
                    # Split the plaincode into groups of 5 digits and send it to the HTML form
                    dec_plaincode = otpyf.split_into_groups_of_five(plaincode)
                    # Decode the plaincode to plaintext and send it to the HTML form
                    dec_plaintext = otpyf.unstraddle(plaincode, checkerboard_manual, checkerboard_manual['F/L'])
                    # Split the ciphertext into groups of 5 digits and send it to the HTML form
                    dec_ciphertext = otpyf.split_into_groups_of_five(ciphertext)
                except Exception as e:
                    # Send any errors to the HTML form
                    status = e
            else:
                # Do nothing if the user did not provide a cipher for decryption. User will be notified via the HTML form.
                status = "Enter the ciphertext for decryption..."
            
    # Render the index.html template with updated encryption/decryption or status data
    return render_template('index.html', 
    enc_plaincode=enc_plaincode, 
    enc_plaintext=enc_plaintext, 
    enc_ciphertext=enc_ciphertext, 
    enc_otp_key=enc_otp_key, 
    enc_otp_key_id=enc_otp_key_id, 
    dec_plaintext=dec_plaintext, 
    dec_plaincode=dec_plaincode, 
    dec_ciphertext=dec_ciphertext, 
    dec_otp_key=dec_otp_key,
    dec_otp_key_id=dec_otp_key_id,
    status=status)

# Define a route for the synth page. Handle both GET and POST requests
@app.route('/synth', methods=['GET', 'POST'])
def synth():
    # Initialize a variable to hold any status messages
    status = ''
    # Handle the POST (form submittion) request.
    if request.method == 'POST':
        # Use `user_input` as the message to be synthesized
        user_input = request.form['input_text']
        if 'message' in request.form:
            # Check if the user entered any message for synthesis
            if user_input:
                # Convert the numbers and alpha sound files (specified in the config) to a python list.
                lst_numbers = numbers.split(', ')
                lst_alpha = alpha.split(', ')
                # Define the directory where the cipher.wav file is stored
                directory = "./"
                # Run the synthesis procedure in a try block to catch any errors
                try:
                    # Synthesize the message
                    synthesizer = otpyf.AudioMessageSynthesizer(user_input, prepend_audio, append_audio, lst_numbers, lst_alpha)
                    synthesizer.construct_wav()
                    # Download the synthesized cipher.wav file
                    return send_from_directory(directory, "cipher.wav", as_attachment=True)
                except Exception as e:
                    # Send any errors to the HTML form
                    status = e
            else:
                # Do nothing if the user did not provide a message for synthesis. User will be notified via the HTML form.
                status = "Enter the message for synthesis..."       
    # Render the index.html template with updated data
    return render_template('synth.html', status=status)

@app.route('/csrng', methods=['GET'])
def csrng():
    crng_pads = otpyf.generate_csrng_numbers(cipher_length + 5, num_pads)
    # Run the CSRNG function in a try block to catch any errors
    try:
        # Save pads for encryption (sending messages)
        otpyf.save_to_jsonline_file("./pads_temp/pads_send.json", crng_pads)
        # Save pads for decryption (receiving messages) 
        otpyf.save_to_jsonline_file("./pads_temp/pads_recv.json", crng_pads)
        return "Data saved successfully to ./pads_temp/ directory.<br>You need to manually exchange the pads_recv.json with the counterpart you're communicating with!"
    # Catch any errors
    except Exception as e:
        # Return any errors to the HTML
        return str(e)

# Define a route for editing the configuration. Handle GET and POST requests
@app.route('/edit-config', methods=['GET', 'POST'])
def edit_config():
    # Define the global variables for the config settings
    global checkerboard, pads_recv, pad_send, cipher_length, num_pads, numbers, alpha, prepend_audio, append_audio
    
    # Handle the POST (form submittion) request.
    if request.method == 'POST':
        # Update config.ini file with the content from the HTML form
        with open('config.ini', 'w') as file:
            file.write(request.form['configContent'])
        
        # Reload the configuration from the updated config.ini file
        config.read('config.ini')
        checkerboard = config['DEFAULT']['checkerboard']
        pads_recv = config['DEFAULT']['pads_recv']
        pad_send = config['DEFAULT']['pad_send']
        cipher_length = int(config['DEFAULT']['cipher_length'])
        num_pads = int(config['DEFAULT']['num_pads'])
        numbers = config['DEFAULT']['numbers']
        alpha = config['DEFAULT']['alpha']
        prepend_audio = config['DEFAULT']['prepend_audio']
        append_audio = config['DEFAULT']['append_audio']

    # Read the current content of config.ini for display in the form
    with open('config.ini', 'r') as file:
        config_content = file.read()

    # Send config.ini content to the HTML form
    return render_template('edit_config.html', config_content=config_content)

# Entry point for running the Flask application
# This is left for debugging purposes. In actual implementation you'll use something like hypercorn
#if __name__ == '__main__':
    # Test HTTPs
    #app.run(host="0.0.0.0", port=443, debug=True, ssl_context=('./cert.pem', './key.pem'))
    #app.run(debug=True)