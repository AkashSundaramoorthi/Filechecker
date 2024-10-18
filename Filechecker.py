import os
import json
import time
import hashlib

hash_values = 'hash_values.json' #this is where it will store the hash values of the file

paths = [ #path for important file location
    r"/etc/Codenex/something.rtf"
]

logs = 'integrity_logs.txt' #this is where the logs of the files go

def calc_hash(path): #calculates the hash of the particular file
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

def load_hash(): #loads previously save hashes 
    if os.path.exists(hash_values):
        return json.load(open(hash_values, "r"))
    return {}

def save_hash(hash_data): #saves the hash data to the file
    json.dump(hash_data, open(hash_values, "w"), indent=4)

def log_change(change_type, path): #to log the changes 
    open(logs, "a").write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {change_type}: {path}\n")

def check_integrity(): #to check the integrity and log the activities of that file
    prev_hash = load_hash()
    current_hashes = {}

    for path in paths:
        current_hash = calc_hash(path)

        if current_hash is None:
            if path in prev_hash:
                log_change("File Deleted", path)
        else:
            current_hashes[path] = current_hash
            if path not in prev_hash:
                log_change("File Added", path)
            elif prev_hash[path] != current_hash:
                log_change("File Modified", path)
    
    save_hash(current_hashes)

while True: #to run infinitely
    check_integrity()
    time.sleep(60 * 10) #checks for every 10 minutes
