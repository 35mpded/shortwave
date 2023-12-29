<p align="center">
  <img src="https://github.com/35mpded/shortwave/blob/main/imgs/demo.png">
</p>

**Shortwave** is an app for covert cryptographic communication. The name of this project is inspired by the [number stations](https://www.youtube.com/watch?v=IlpOMkuTwmU), known for their unique broadcasts of random number sequences over **shortwave radio**. These number sequences are actually covert messages encrypted with the One-Time Pad cipher, the only cipher that is proven to be unbreakable. The **Shortwave** app adopts this same encryption technique by using the [OTPy Framework](https://github.com/35mpded/otpy-framework).

> If you're new to the One-Time Pad cipher, you can learn about it by reading [The One-Time Pad Cipher](https://github.com/35mpded/otpy-framework/blob/main/docs/the_otp_cipher.md) introduction or by watching [The ULTIMATE One Time Pad Tutorial](https://www.youtube.com/watcth?v=rCeWtQERizA&lc=UgxNO0gFvF-qLf0YiYF4AaABAg.9y0-NsbHT239yEB73sMyWK).

**WARNING:**<br>
*The Shortwave app is designed for Local Area Network (LAN) hosting only. **You should never host or use the Shortwave app on internet connected devices.** You can use a standalone single-board computer (SBC) like the Raspberry Pi or something similar for this purpose, then access the application through LAN. Furthermore, using the cipher on the internet leaves a digital footprint, which means that while the cipher itself may be unbreakable, the encrypted messages could still be traced back to you.*

# Features
*The **Shortwave** is equipped with number of features to aid you in the correct use of the One-Time Pad cipher. However, it will not (and cannot) prevent you from doing stupid sh\*t like leaking or reusing your OTP keys. The responsibility of safeguarding your keys and adhering to best practices is entirely on you!* 

-   Encode and Decode messages through the use of a checkerboard.
-   Easily create & use custom checkerboards through CSV files.
-   Generate and store cryptographically secure OTP keys as JSON Lines files.
-   Encrypt and Decrypt messages through modulus 10.
-   OTP key management with automated Selection and Disposal of Encryption/Decryption keys.
-   Synthesize ciphertext to speech, enabling transmission over audio mediums such as radio (number stations), YouTube, and whatever.

# Installation
If you would like to use the message synthesizer (which is entirely optional), follow the instructions provided in the **Synthesizer setup** section of this page.
1. Download the **Shortwave** app by entering the terminal command `git clone https://github.com/35mpded/shortwave.git && cd shortwave`
2. Install the requirements `python3 -m pip install -r requirements.txt`
	>*Install pip3 if you don't already have it `sudo apt install python3-pip`* 
3. Generate the HTTPs certificate. Instructions are provided in the **Certificate setup** section of this page.
4. Run the application `sudo hypercorn shortwave:app --bind 127.0.0.1:443 --keyfile ./key.pem --certfile ./cert.pem`
	>*Replace the 127.0.0.1 with your private IP address to make the app accessible over the Local Area Network (LAN)*
5. Configure the application. Instructions are provided in the **Configuration** section of this page.


# Synthesizer setup

The synthesizer is an optional feature of the **Shortwave** app that allows you to convert your cipher messages to audio. If you want to use this feature, you'll need to download the voice data from the vocoder repository. Follow the below steps to setup the message synthesizer:
1. Open a terminal inside the **Shortwave** web app directory or CD into it.
2. Download the voice data `git clone https://github.com/35mpded/otpy-vocoder-data.git`
3. Move the `./vo` directory inside the **Shortwave** app directory `mv ./otpy-vocoder-data/vo/ .`

The shortwave app should now be ready to synthesize your messages.
***
**Custom voice pack:**<br>
You can create your own voice pack for the message synthesizer by using [Audacity](https://www.audacityteam.org/), an open-source audio editing software. The message synthesizer works with the following audio files:
- Mono
- Samle rate 22050Hz
- Exported as .WAV - 16-bit PCM

Free sound packs can be downloaded from [freesound.org](https://freesound.org/)

# Certificate setup
The **Shortwave** app should be hosted on an HTTPs-enabled server to protect against Man-in-the-middle (MITM) attacks on the LAN. However, this requires you to generate a certificate by following the instructions provided below:
> Be aware that HTTPs will protect you from MITM (Man-in-the-middle) attacks but nothing more than that.  You should never host or use the app outside of the Local Area Network (LAN)

1. Open a terminal inside the **Shortwave** app directory or CD into it.
2. Generate the certificate by entering the terminal command `openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/CN=shortwave.local"`
3. Verify whether the certificate was successfully generated  by using `openssl x509 -in cert.pem -text -noout`

# Checkerboard
The Shortwave app enables you to create and use your own checkerboards through any CSV file that follows the format of the provided examples at_one_sir.csv and xray.csv. These examples can be found in the `./checkerboards` directory of the **Shortwave** app.

**AT ONE SIR:**
|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8   | 9   |
|---|---|---|---|---|---|---|---|---|-----|-----|
|   | A | T |   | O | N | E |   | S | I   | R   |
| 2 | B | C | D | F | G | H | J | K | L   | M   |
| 6 | P | Q | U | V | W | X | Y | Z | F/L | /   |

**XRAY:**
|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8   | 9   |
|---|---|---|---|---|---|---|---|---|-----|-----|
|   | X | R | A | Y |   |   |   |   |     |     |
| 4 | B | C | D | E | F | G | H | I | J   | K   |
| 5 | L | M | N | O | P | Q | S | T | U   | V   |
| 6 | W | Z | ~ | ` | ! | @ | # | $ | %   | ^   |
| 7 | & | * | ( | ) | _ | - | + | = | [   | ]   |
| 8 | { | } | \ | \| | ; | : | ' | " | ,   | <   |
| 9 | . | > | / | ? | ° | ♥ | ■ |   | F/L | SPC |

There are some key points to keep in mind while crafting a custom checkerboard:
- 'SPC' and 'F/L' are reserved designations for special purposes, yet their inclusion in the checkerboard is only optional.
	- 'SPC' is used to indicate whitespace (0x20).
	- 'F/L' is used to indicate letter/figure switch (A-Z/0-9).
- Empty fields will not break your checkerboard, as long as they're within the grid boundaries.
- Theoretically, you can use any character supported by your environment, such as special symbols, non-Latin characters, and so on.

# Configuration
While the Shortwave app is automated (for the most part), there are some settings and things you must take care of before using it.
> Remember that the One-Time Pad is a cipher intended for use between two parties. The configuration you apply must also be replicated by your counterpart.


1. You and your counterpart need to agree on which checkerboard you'll both use.  More information can be found in the checkerboard section of this page.
	- Open the  `config.ini` configuration file and modify the default `checkerboard` value to the one you've agreed upon with your counterpart.
2. You and your counterpart need to agree on the maximum length of the cipher messages
	- Open the `configini` configuration file and modify the default `cipher_length` value to the one you've agreed upon with your counterpart.
3. You and your counterpart need to agree on the maximum number of messages that'll be sent before having to generate a new key.
	- Open the `config.ini` configuration file and modify the default `num_pads` value to the one you've agreed upon with your counterpart.
		> Be careful with this option since very large numbers can generate very large files.
5. Generate and exchange the OTP keys.
	- Visit the following URL `https://<your_local_address>/CSRNG`. This will generate the JSONL files with OTP keys inside the `./pads_temp` directory. 
	- Securely exchange the keys with your counterpart, preferably through a physical method such as a USB stick. You'll need to give them your pad_recv.json file, and in return, they should provide you with their pad_recv.json file
	- Add your counterpart's `pad_recv.json` to the `./pads_in` directory and your own `pad_send.json` in the `./pads_out` directory.<br>*You can rename the `pad_send.json` but you need to reflect the change inside the config.ini file.*

That's it. You can now encrypted & decrypt messages using the Shortwave app.

# Functions
The **Shortwave** application doesn't have a menu for easy navigation to its various functions. However, you can still access these functions by using the provided links below:
- For encrypting or decrypting messages, please go to this endpoint: `https://<your_local_address>/`
- To generate cryptographically secure one-time pads, navigate to this endpoint: `https://<your_local_address>/csrng`
- If you wish to synthesize messages, simply visit this endpoint: `https://<your_local_address>/synth`
- To make configuration edits through the web server, access the following endpoint: `https://<your_local_address>/edit-config`
