import os
import time
import numpy as np
import pandas as pd
import joblib
import shutil
import pyfiglet

xgb_model = joblib.load("xgb_model.joblib")

a = '"0","1","2","3","4","5","6","7","8","9","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff","??","size"'
columns = a.strip('"').split('","')  


def convert_bytes_to_txt(file):
    if(file.endswith("bytes")):
        shutil.copyfile(file, file.split('.')[0] + "_copy.bytes")
        time.sleep(1) 
        file=file.split('.')[0]
        text_file = open(file+".txt", 'w+')
        with open(file+".bytes","r") as fp:
            lines=""
            for line in fp:
                a=line.rstrip().split(" ")[1:]
                b=' '.join(a)
                b.lower()
                b=b+"\n"
                text_file.write(b)
            fp.close()
            os.remove(file+".bytes")
        text_file.close()
        os.rename(file+"_copy.bytes",file+".bytes")

def convert_to_lowercase(input_str):
    output_str= ""
    if input_str[0]=='0' and input_str[1].isdigit():
        return input_str[1:]
    if input_str[0].isdigit() and input_str[1].isdigit():
        return input_str
    if len(input_str) == 2 and input_str[0].isupper() and input_str[1].isdigit():
        output_str = input_str[0].lower() + input_str[1]
        return output_str
    if len(input_str) >= 2 and input_str[0].isdigit() and input_str[1].isupper():
        output_str = input_str[0] + input_str[1].lower()
        return output_str
    if len(input_str) == 2 and input_str[0].isupper() and input_str[1].isupper():
        output_str = input_str[0].lower() + input_str[1].lower()
        return output_str
    else:
        return input_str
    
def predict_malware(file_path):
    print(len(columns))
    file_features = np.zeros((1, len(columns)))  
    with open(file_path, "r") as fp:
        for lines in fp.readlines():
            line = lines.rstrip().split(" ")[1:]
            for hex_code in line:
                if hex_code == '??':
                    file_features[0][columns.index("??")] += 1
                else:
                    file_features[0][columns.index(convert_to_lowercase(hex_code))] += 1
        statinfo = os.stat(file_path)
        file_size_mb = statinfo.st_size / (1024 * 1024)
        file_features[0][columns.index("size")] = file_size_mb
    
    file_df = pd.DataFrame(file_features, columns=columns)  
    prediction = xgb_model.predict(file_df)

    return ("Predicted class:", prediction[0])

def start():
    os.system("cls")
    print(pyfiglet.figlet_format("Welcome"))
    print("1. Find the class of Malware in .bytes file")
    print("2. Predict Malware")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        # Get the file name from the user
        file_name = input("Enter the name of the .bytes file: ")
        # Convert the bytes file to text
        convert_bytes_to_txt(file_name)
        print("Conversion complete. Text file created.")
        time.sleep(2)
        prediction = predict_malware(file_name)
        print("Prediction:", prediction)
        time.sleep(2)
        
    elif choice == "3":
        print("Exiting...")
        time.sleep(2)
        exit()
    else:
        print("Invalid choice")
        time.sleep(2)
    # Ask user if they want to continue
    continue_choice = input("Do you want to continue? (y/n): ").lower()
    if continue_choice == 'y':
        start()
    elif continue_choice == 'n':
        print("Exiting...")
        time.sleep(2)
        exit()
    else:
        print("Invalid choice. Exiting...")
        time.sleep(2)
        exit()

# Call the start function to begin the program
start()