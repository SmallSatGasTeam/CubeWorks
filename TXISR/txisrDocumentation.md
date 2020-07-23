GASPACS Software III: The TXISR
==
Interrupt:
--
Location: ../TXISR/interrupt.py

Functionality: The code that comprises the Interrupt does one thing. When a transmission comes from a ground station it will interrupt what is happening on the Raspberry Pi so that we can handle the transmissions to and from the ground. After the interrupt, the software will then go to the TX/RX stage.

TX/RX (Transmit and Receive):
--
Location: ../TXISR/rxHandling.py 

Functionality: The TX/RX stage does the main bulk of the work needed to be done in order to transmit a message back to the ground. During this stage the software will:
Decode the message received from the ground. 
Determine the type of packets or data requested.
Get the queried data from the database, packetize data and write the data to a file.
Determine from the received message when the transmission window will start.
Determine how long the transmission window will last.
Then wait till five seconds before the scheduled window for transmission. 

NOTES:
--
The data will be data collected by the Drivers (see GASPACS Software I: The Drivers).
For more information on transmissions from the ground see GASPACS Flight Logic Plan Outline Appendix C Tables 5, 6 and 7. 
For information on transmissions to the ground see GASPACS Flight Logic Plan Outline Appendix B Tables 1, 2, 3 and 4.  

