# The file main_interface is the interface of the program to interact with the user.

# Import functions module and modules need to run the main interface
import serial
import serial.tools.list_ports
from functions import *
from record import recordFromSTM
import subprocess
import pygame
import os

# Define global variables 
foundPort = get_ports()
connectedPort  = findSTM32(foundPort)

# The main function is to run the whole interface system 
def main(): 
    print("...Start the program...\n")
    while True: 
        try: 
            if connectedPort != 'None': 
                # keep checking connection with STM32
                ser = serial.Serial(connectedPort,115200,timeout=1)
                print("\nSTM32 is connected\n")
                print("1. Record audio manually")
                print("2. Report data")
                print("3. Record audio depending on distance from the user")
                print("4. Implement moving average filter ")
                print("5. Play the audio")
                option = input("\nplease choose the number : ")

                # condition statements to run the mode chosen by user 
                if option == '1': 
                    print("\nOptions available are\n ")
                    print("1. Press ctrl+C to stop record")
                    print("2. Record in the chosen duration ")
                    recordOption = input("\nplease choose : ")
                    if recordOption == '1': 
                        option_one_press_stop()
                    elif recordOption == '2': 
                        option_one_chosen_duration()
                    else: 
                        print("invalid number, please enter the number again")
                        recordOption = input("\nplease choose : ")
                elif option == '2': 
                    option_two()
                elif option == '3':
                    option_three()
                elif option == '4': 
                    option_four()
                elif option == '5': 
                    option_five()
                else: 
                    print("invalid number, please enter the number again")
                
            else: 
                print("STM32 is not connected")
                print("Program cannot proceed, please check connection")
                break
        except OSError: 
        # lost connection with STM32
            print("STM32 is disconnected")
            print(e)
            ser.close()
            break
        except KeyboardInterrupt: 
            print("\n...End program...")
            ser.close()
            break 

# The option_one_press_stop function is to let the user start and stop recording by themselves
def option_one_press_stop(): 
    try: 
        print("\n...Start recording...")
        #send command to stm32 to run voltage part in cubeIDE 
        command = 'R'
        send_to_uart(command,connectedPort) 
        #record.py 
        record(connectedPort)
        #csv_to_wav file 
        print("...WAV file is being generated...")
        os.system("./c_processing_program/csv_to_wav python_interface_and_output_file/output.DATA python_interface_and_output_file/output.wav")
    except KeyboardInterrupt: 
        print("...exit mode...")

# The option_one_chosen_duration function is to let the user set the duration of the audio 
def option_one_chosen_duration(): 
    try: 
        audioDuration = int(input("\nPlease set audio duration(s): "))
        print("\n...Start recording...")
        #send command to stm32 to run voltage part in cubeIDE 
        command = 'R'
        send_to_uart(command,connectedPort) 
        os.system(f"python3 python_interface_and_output_file/record.py port={connectedPort}")
        recordFromSTM(connectedPort, baud=115200, duration=audioDuration)
        #csv_to_wav file 
        print("...WAV file is being generated...")
        os.system("./c_processing_program/csv_to_wav python_interface_and_output_file/output.DATA python_interface_and_output_file/output.wav")
    except KeyboardInterrupt: 
        print("\n...exit mode...")

# The option_two function is to report sampling rate used, recorded audio duration and graph 
def option_two(): 
    try: 
        print("\n...Reporting Data...\n ")
        #audioLength = get_time_duration()
        #print("Audio length : ", audioLength, "s")
        print("Sampling rate : ")
        filename = '../python_interface_and_output_file/output.DATA'
        generate_graph_csv(filename)
    except KeyboardInterrupt: 
        print("\n...exit mode...")
    except AttributeError: 
        print("\n...exit mode...")

# The option_three function is to let the user record depending on the distance read from ultrasoic sensor
def option_three(): 
    try: 
        #send command to stm32 to run ultrasonic part
        command = 'U'
        send_to_uart(command,connectedPort)
        print("\n...Detecting distance from user...")
        print("Please select distance range ")
        minDistance = int(input("choose minimum distance: "))
        maxDistance = int(input("choose maximum distance: "))
        #record_depend_distance(connectedPort, minDistance, maxDistance)
        record(connectedPort)
        #csv_to_wav file 
        print("...WAV file is being generated...")
        os.system("./c_processing_program/csv_to_wav_run python_interface_and_output_file/output.DATA python_interface_and_output_file/output.wav")

    except KeyboardInterrupt: 
        print("\n...exit mode...")

# The option_four function is to let the user implement moving average filter with data recorded from STM32
def option_four():
    try: 
        print("\n...Implementing moving average filter...")
        #call make file and run implement_moving_average
        os.system("./c_processing_program/moving_average_impl")
        print("\nfiltered data is stored in the moving_average_result.txt, please to open the file to see the result")
        generate_graph_csv("python_interface_and_output_file/output.DATA", "python_interface_and_output_file/voltage_vs_time_plot.png")
        generate_graph_csv("python_interface_and_output_file/moving_average_result.csv", "python_interface_and_output_file/_moving_averagevoltage_vs_time_plot.png")
    except KeyboardInterrupt: 
        print("\n...exit mode...")
    except FileNotFoundError: 
        print("please check current directory")
        
# The option five function is to let the user play the audio from WAV file
def option_five(): 
    try: 
        audioFile = "../python_interface_and_output_file/output.wav"
        play_audio(audioFile)
    except pygame.error: 
        print("Error opening file")
    except KeyboardInterrupt: 
        print("Stop playing by user")
        print("\n...exit mode...")

# Statement to run the system 
if __name__ == "__main__": 
    main()
    
