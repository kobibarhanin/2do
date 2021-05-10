import hashlib 

def get_sha(text):  
    result = hashlib.sha256(text.encode())      
    return result.hexdigest()