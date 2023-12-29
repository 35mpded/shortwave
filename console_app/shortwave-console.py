import otpyf
import configparser

# Initialize the configparser and read settings from 'config.ini'
config = configparser.ConfigParser()
config.read('config-console.ini')

# Retrieve the settings from the config file
checkerboard = config['DEFAULT']['checkerboard']
pads_recv = config['DEFAULT']['pads_recv']
pad_send = config['DEFAULT']['pad_send']
cipher_length = int(config['DEFAULT']['cipher_length'])
num_pads = int(config['DEFAULT']['num_pads'])
num_pads = int(config['DEFAULT']['num_pads'])
numbers = config['DEFAULT']['numbers']
alpha = config['DEFAULT']['alpha']
prepend_audio = config['DEFAULT']['prepend_audio']
prepend_audio = config['DEFAULT']['prepend_audio']
append_audio = config['DEFAULT']['append_audio']

# Build and print the Text menu
def print_menu():
    otpyf.clear()
    print (20 * "=" , "SHORTWAVE" , 20 * "=")
    print ("[1] ENCRYPT A MESSAGE \n[2] DECRYPT A MESSAGE \n[3] GENERATE A RANDOM PAD\n[4] SYNTHESIZE A MESSAGE")
    print (51 * "=")
loop=True

while loop:
    # Print the menu while the loop is active
    print_menu()
    choice = input("\nSelect an action [1-4]: ")
   
    if choice == "1":
        # Clear the screen so that it's nice to read
        otpyf.clear()
        # Inform the user that the checkerboard is being loaded
        print("[*] LOADING CHECKERBOARD: " + checkerboard)
        # Load the checkerboard from the CSV file specified in the config.ini
        checkerboard_manual = otpyf.csv_checkerboard_to_dict(checkerboard)
        # Print the loaded checkerboard into a nice text table
        print("[*] USING CHECKERBOARD:\n")
        otpyf.print_checkerboard_table(checkerboard)
        # Prompt the user for a message that'll be encoded & encrypted
        input_plaintext = input("\n[*] ENTER A MESSAGE TO ENCRYPT: \n$ ")
        # Encode the message to plaincode
        plaincode = otpyf.straddle(input_plaintext, checkerboard_manual, checkerboard_manual['F/L'], cipher_length)
        # Print the plaincode in groups of 5 digits and its length  
        print(f"\n[*] PLAINCODE (LENGTH {len(plaincode)}):")
        print(otpyf.split_into_groups_of_five(plaincode))
        # Decode the plaincode and print it for visual verification by the user
        de_plaintext = otpyf.unstraddle(plaincode, checkerboard_manual, checkerboard_manual['F/L'])
        print("\n[*] PLAINTEXT:\n" + de_plaintext)
        # Ask the user if they want to proceed with encryption
        proceed_to_encrypt = input("\n[*] DO YOU WANT TO ENCRYPT THIS MESSAGE? (Y/N): \n$ ").strip().upper()
        if proceed_to_encrypt == "Y":
            # Run the encryption procedure in a try block to catch any errors, such as unavailable and/or malformatted encryption pad (key) or file
            try:
                # Encrypt the plaincode by using a random pad from the specified jsonl file
                encrypted_message, otp_key, otp_key_id = otpyf.encrypt_init(pad_send, plaincode, cipher_length)
                # Provide the user with the encryption pad (key) that will be used for encryption
                print(f"\n[*] ONE-TIME PAD ENCYPTION KEY:\n({otp_key_id}) " + (otpyf.split_into_groups_of_five(otp_key)))
                # Provide the user with the ciphertext (encrypted message) split into groups of 5 digits (for readability)
                print(f"\n[*] CIPHERTEXT (LENGHT {len(encrypted_message)}):")
                print(otpyf.split_into_groups_of_five(encrypted_message))
                # After the encoding and encryption are done, warn the user that they'll go back to the main menu and lose the ciphertext
                print("\n[*] WARNING:\nWRITE DOWN OR COPY THE CIPHERTEXT NOW, OTHERWISE YOU'LL LOSE IT IRREVERSIBLY!")
                input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
            except Exception as e:
                # In case of an error let the user know
                print("\n[*] ERROR:")
                print(e)
                input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
        elif proceed_to_encrypt == "N":
            input("\n[*] SKIPPING ENCRYPTION\n\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
        else:
            input("\n[*] INVALID RESPONSE\n\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
        otpyf.clear()

    elif choice=="2":
        # Clear the screen so it's nice to read
        otpyf.clear()
        # Inform the user that the checkerboard is being loaded
        print("[*] LOADING CHECKERBOARD: " + checkerboard)
        # Load the checkerboard from the CSV file specified in the config.ini
        checkerboard_manual = otpyf.csv_checkerboard_to_dict(checkerboard)
        # Print the loaded checkerboard into a nice text table
        print("[*] USING CHECKERBOARD:\n")
        otpyf.print_checkerboard_table(checkerboard)
        # Prompt the user for the ciphertext which will be decrypted and decoded
        input_ciphertext = input("\n[*] INPUT THE CIPHERTEXT FOR DECRYPTION:\n$ ").replace(" ", "")
        # Run the deccryption procedure in a try block to catch any errors, such as unavailable and/or malformatted encryption pad (key) or file
        try:
            # Inform the user that the program is searching for a decryption key
            print("\n[*] SEARCHING FOR THE DECRYPTION KEY IN: " + pads_recv)
            # Initialize the decryption procedure
            decrypted_message, otp_key, otp_key_id = otpyf.decrypt_init(pads_recv, input_ciphertext)
            # Provide the user with the decryption pad (key) that will be used.
            print(f"\n[*] ONE-TIME PAD DECRYPTION KEY:\n({otp_key_id}) " + (otpyf.split_into_groups_of_five(otp_key)))
            # Provide the user with the decrypted plaincode
            print("\n[*] PLAINCODE:\n" + (otpyf.split_into_groups_of_five(decrypted_message)))
            # Provide the user with the plaintext (decoded message)
            dePlaincode2 = otpyf.unstraddle(decrypted_message, checkerboard_manual, checkerboard_manual['F/L'])
            print("\n[*] PLAINTEXT:\n" + dePlaincode2)
             # After the decryption and decoding are done, warn the user that they'll go back to the main menu.
            print("\n[*] WARNING:\nWRITE DOWN OR COPY THE PLAINTEXT NOW, OTHERWISE YOU'LL LOSE IT IRREVERSIBLY!")
            input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
        except Exception as e:
            # In case of an error let the user know
            print("\n[*] ERROR:")
            print(e)
            input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")

    elif choice=="3":
        # Clear the screen so that it's nice to read
        otpyf.clear()
        # Generate the cryptographically secure pseudorandom numbers
        print("[*] GENERATING ONE-TIME PADS...")
        # Store the CSRNG into a variable
        crng_pads = otpyf.generate_csrng_numbers(cipher_length, num_pads)
        # Let the user knows that X ammount of pads each with Y Key lenght have been generated
        print ("\n[*] GENERATED " + (str(num_pads) + " ONE-TIME PADS EACH WITH KEY LENGHT OF " + str(cipher_length + 5)))
        # Write the OTP keys to jsonl files
        # Create the jsonl files in a try block to avoid overwriting existing jsonl files.
        try:
            # Inform the user that the OTP keys are being written to jsonl files
            print("\n[*] SAVING ONE-TIME PADS...")
            # Write the keys to JSONL files
            # Save pads for encryption (sending messages)
            otpyf.save_to_jsonline_file("./pads_temp/pads_send.json", crng_pads)
            # Save pads for decryption (receiving messages) 
            otpyf.save_to_jsonline_file("./pads_temp/pads_recv.json", crng_pads)
            # Inform the user that the files were written successfully
            print("Pads successfully written to './pads_temp/'\n")
            print("\n[*] WARNING:")
            print("You need to manually exchange the pads_recv.json with the counterpart you're communicating with!")
        # Check if the jsonl files already exist to avoid overwriting them
        except FileExistsError as e:
            print("\n[*] ERROR:")
            print(e)
        input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
    # In case the user makes an invalid choices
    elif choice=="4":
        # Clear the screen so that it's nice to read.
        otpyf.clear()
        # Convert the numbers and alpha sound files (specified in the config) to a python list
        lst_numbers = numbers.split(', ')
        lst_alpha = alpha.split(', ')
        # Request  message that'll be synthesized
        input_synthesize = input("\n[*] INPUT A MESSAGE TO SYNTHESIZE: \n$ ")
        # Synthesize the input
        synthesizer = otpyf.AudioMessageSynthesizer(input_synthesize, prepend_audio, append_audio, lst_numbers, lst_alpha)
        synthesizer.construct_wav()
        input("\nPRESS ENTER TO RETURN IN MAIN MENU...\n")
    # In case the user makes an invalid choices
    else:
       input("\nThis action does not exist. Press enter key to continue...")
