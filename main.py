import re
import hashlib
import requests
import pandas as pd
import random
import string
from flask import Flask, request,jsonify

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            break
    return password

def calculate_password_score(password):
    # Length (L)
    global L
    L = 0
    length = len(password)
    if length < 10:
        L += 0
    elif length == 10:
        L += 25
    elif 10 < length <= 12:
        L += 75
    elif length > 12:
        L += 100

    # Complexity (C)
    global C
    C = 0
    if re.search(r'[A-Z]', password):
        C += 25
    if re.search(r'[a-z]', password):
        C += 25
    if re.search(r'\d', password):
        C += 25
    if re.search(r'[^A-Za-z0-9]', password):
        C += 25

    if C < 75:
        C = 0


    # Variability (V)
    global V
    V=0
    if re.search(r'(.)(\1\1)', password):
        V = 0
    else:
        V = 100


    # Uniqueness (U)
    global U
    U=0
    common_file = pd.read_csv(r"C:\Users\asus\Desktop\Project Security\common_passwords.csv")
    common_pwd = common_file['password'].tolist()
    # Check if the password is in the dictionary list
    if password in common_pwd:
        U = 0
    else:
        U = 100

    # Dictionary Words (D)
    global D

    D=0
    dic_file = pd.read_csv(r"C:\Users\asus\Desktop\Project Security\dictionary_words.csv")
    dictionary_word = dic_file['word'].tolist()
    if (any(word in password for word in dictionary_word)) or (any(word in password for word in common_pwd)):
        D = 0
    else:
        D = 100

    # Leaked Password Detection Algorithm (leaked)
    global leaked
    leaked = 0;
    api_url = "https://api.pwnedpasswords.com/range/"
    # Hash the password using SHA-1 algorithm
    password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Call Have I Been Pwned API
    request = requests.get(api_url + password_hash[:5])
    # Check if password hash is in Have I Been Pwned DB
    is_cracked = password_hash[5:] in [x.split(":")[0] for x in request.text.split("\n")]
    # Print result
    if is_cracked:
        leaked =0 ;
    else:
        leaked = 100;

    # Calculate overall score based on weights
    #  weights = {'L': 0.15,'C': 0.10,'V': 0.10,'U': 0.20,'D': 0.20,'Leaked': 0.25}
    score = L*0.15+C*0.1+V*0.1+U*0.2+D*0.2+leaked*0.25
    return score

def password_score_evaluation(score):
    if score <= 40:
        return "Your password is Weak"
    elif score <= 70:
        return "Your password is Medium"
    elif score <= 90:
        return "Your password is Good"
    else:
        return "Congratulation! your password is Strong"


def feedback(password):
    feedback = ""
    # Length (L) check
    if L < 10:
        feedback += "The password should be at least 10 characters long."
    # Complexity (C) check
    if C == 0:
        feedback += "The password should include a combination of uppercase letters, lowercase letters, numbers, and special characters."

    # Variability (V) check
    if V == 0:
        feedback += "Avoid using three or more identical characters consecutively in the password."

    # Uniqueness (U) check (Assuming known_passwords is a list of known passwords)
    if U == 0:
        feedback += "The password is not unique : Avoid using commonly used passwords!"

    # Dictionary Words (D) check (Assuming dictionary_words is a list of dictionary words)
    if D==0:
        feedback += "The password contains common dictionary words: Avoid using dictionary words!"

    # Leaked Password Detection (leaked) check
    if leaked== 0:
        feedback += "The password has been previously leaked : Choose a different, unique password!"
    x=print(feedback)
    return x

app = Flask(__name__)
@app.route('/evaluate-password', methods=['POST'])
def evaluate_password():
    password = request.form.get('password')
    score = calculate_password_score(password)
    evaluation = password_score_evaluation(score)
    feedback_text = feedback(password)
    response = {
        'score': score,
        'evaluation': evaluation,
        'feedback': feedback_text
    }
    return jsonify(response)
if __name__ == '__main__':
    app.run()