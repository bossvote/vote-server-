from flask import Flask, request, jsonify
import json, os, requests

app = Flask(__name__)

FILE = "users.json"
poll_votes = {"A": 0, "B": 0, "C": 0, "D": 0}
quiz_votes = {"1": 0, "2": 0, "3": 0, "4": 0}

if os.path.exists(FILE):
    with open(FILE, 'r') as f:
        saved_users = json.load(f)
else:
    saved_users = []

def check_insta_real(username):
    try:
        # Instagram public page check
        url = f"https://www.instagram.com/{username}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=8)
        # Agar page mile aur "Sorry" wala page na ho to real hai
        if r.status_code == 200 and 'profilePage_' in r.text or '"username":"'+username+'"' in r.text or f'"{username}"' in r.text and "Sorry, this page isn't available" not in r.text:
            return True
        # Second check: 200 aaya to real maan lete hai
        if r.status_code == 200:
            return True
        return False
    except:
        return False

@app.route("/")
def home():
    return f"""
    <h1>Vote Server LIVE 🔥</h1>
    <p>Total Saved Real IDs: {len(saved_users)}</p>
    <form action="/login">
        <input name="insta_id" placeholder="Real Instagram ID likho" required>
        <button>Check & Save</button>
    </form>
    <h2>ABCD Vote</h2>
    <a href="/vote?type=poll&option=A"><button>A</button></a>
    <a href="/vote?type=poll&option=B"><button>B</button></a>
    <a href="/vote?type=poll&option=C"><button>C</button></a>
    <a href="/vote?type=poll&option=D"><button>D</button></a>
    <h2>1234 Vote</h2>
    <a href="/vote?type=quiz&option=1"><button>1</button></a>
    <a href="/vote?type=quiz&option=2"><button>2</button></a>
    <a href="/vote?type=quiz&option=3"><button>3</button></a>
    <a href="/vote?type=quiz&option=4"><button>4</button></a>
    <br><br><a href="/result">Result Dekho</a>
    """

@app.route("/login")
def login():
    insta_id = request.args.get("insta_id","").strip().replace("@","")
    if not insta_id:
        return "ID likho Malik!"

    if insta_id in saved_users:
        return f"<h2>{insta_id} Pehle se Saved hai Malik!</h2><a href='/'>Home</a>"

    is_real = check_insta_real(insta_id)

    if is_real:
        saved_users.append(insta_id)
        with open(FILE, 'w') as f:
            json.dump(saved_users, f)
        return f"<h2>✅ {insta_id} Real hai! Save Ho Gaya (Unlimited)</h2><a href='/'>Home</a>"
    else:
        return f"<h2>❌ {insta_id} Fake hai / Instagram pe nahi hai! Login Fail</h2><a href='/'>Wapas try karo</a>"

@app.route("/vote")
def vote():
    t = request.args.get("type")
    o = request.args.get("option")
    if t == "poll" and o in poll_votes: poll_votes[o] += 1
    if t == "quiz" and o in quiz_votes: quiz_votes[o] += 1
    return f"<h2>Vote {o} ko diya!</h2><a href='/'>Home</a>"

@app.route("/result")
def result():
    return jsonify({"total_real_ids": len(saved_users), "saved_ids": saved_users, "poll_ABCD": poll_votes, "quiz_1234": quiz_votes})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
