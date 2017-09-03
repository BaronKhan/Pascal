Pascal
=============

*Pascal* is a personal assistant and room automation system. Similar to Google Home and Amazon Echo,
it is capable of controlling devices in the room, as well as providing small talk and various bits of
information that the user asks. It is named after the machine from the video game, *NieR: Automata*.

Say hello or Pascal's name, followed by a query, such as a greeting, a question, or a command.

Examples of voice requests include:
- "Hello, how are you?"
- "Pascal, what's the weather like tonight?"
- "Hi, who is you master?"
- "Hey Pascal, turn on my fan."
- "Pascal, switch my lamp off."

Room automation is achieved by using a 433MHz RF transmitter to toggle the connected devices, such as
lamps, light bulbs, fans, etc, by simulating the RF signal pulses sent from the bundled RF remote control.

## Hardware

- Raspberry Pi 3
- Raspberry Pi Official 7" Touch Display
- USB Microphone
- Portable Mini Speaker
- 433MHz RF Transmitter
- ZAP 5LX Remote Control Sockets (5x)

## Software

- [snowboy](https://github.com/Kitt-AI/snowboy) - detects the "Hey Pascal" hotword phrases
- [Houndify](https://www.houndify.com) - cloud service for fro request handling
- [gTTs](https://github.com/pndurette/gTTS) - Google Text-to-Speech API