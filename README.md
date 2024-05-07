# Homie-Bot

*By Arnika Abeysekera, Devinn Chi, Quang Nguyen*


## About our project - "HomieBot - The Homie-fication of AI"

When we think about the current state of AI and its recent rise in popularity and usage, we imagine chat bots like ChatGPT. It is easy to understand how useful a tool like this is, but how accessible is it? Initially, our group, Arnika Abeysekera, Quang Aethermai, and Devinn Chi, set out with the goal of creating an interface where a computer could effectively communicate with a LEGO® MINDSTORMS® EV3 robot through morse code, and use a Large Language Model to generate a conversation between person and machine. Our idea was for a separate computer to be able to act as a morse code transmitter, and the EV3 to have the ability to convert the morse code into plaintext, and generate a conversational response, then speak this response back to the user in either morse code or vocally. However, as we considered the practicality of this ambition, we decided to alter our path towards creating an interface that would allow for vocal conversation with AI, through the likeness of an EV3 robot.\

Our idea of setting up an EV3 robot as an interface of communication between person and machine has many real-world applications, as one might imagine. While the purpose of our project was to create an interface in which a user could effectively communicate with an EV3 robot in a conversational manner, one could easily tweak our product and create an assistive AI robot for many different applications. This technology could allow us to be better able to complete our own tasks with the added benefit of machine learning. 
Interaction with generative AI without the need for direct interaction with a computer screen can also be beneficial for people with visual and physical impairments as well, opening up our project’s applicability to cater towards numerous other potential users.


For more information about our project and to read about the modifications we made, check out our project writeup at: 
https://docs.google.com/document/d/1i9SIPJ0HSpCVp0BtW2YP_JNcvx0p7v1RQpOW9lSxpds/edit?usp=sharing


## How To Run

1. Download the dependencies needed to run the project:
```bash
$ pip install -r requirements.txt
```
2. Open OLlama app to run in background so that when model is loaded, OLlama availability will be recognized.
3. Connect the laptop and EV3 via usb cable. 
4. Initiate a wired connection on the EV3 through network settings. 
5. Get the wired IPV4 address, starting with '169.254.xx..' and replace this IP address in `compClient.py` where the comment says "IMPORTANT."
6. Refresh and Download all files to EV3. 
7. Run the`EVServer.py` class in the EV3 SSH terminal. Make sure to use command "cd" to navigate to working directory.
8. Run the `compClient.py` class in IDE of choice terminal and follow the prompts. 

NOTE: There are a lot of issues initating a connecting with the EV3, due to its hardware limitations. While the above steps work in theory, occasionally the connection still fails. Starting the process over should help. 