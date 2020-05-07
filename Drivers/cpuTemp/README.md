# Cpu Temp Driver Documentation
## Requirements
Get the cpu temperature of the raspberry pi and return it to be stored in a dict
## Design
Using the pipe open menthod of the os module(os.popen) get the cpu temperature system variable
## Implementation
1. Pipe open the vcgencmd measure_temp variable and read the line  
2. The variable is formated at "temp=<float>'C"  
3. Replace the "temp=" and "'C" with whitespace and convert the remaining string to a float
4. Return the float
## Testing
* Running the code returns a float everytime the method is called  
* The value of the float is reasonable as a cpu temperature