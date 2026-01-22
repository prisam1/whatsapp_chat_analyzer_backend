from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import re
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    lines = text.split('\n')
    
    # Regex for: M/D/YY, H:MM AM/PM - User: Message
    msg_regex = r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s[APM]{2})\s-\s(.*?):\s(.*)$'
    
    logs = []
    user_days = {}

    for line in lines:
        match = re.match(msg_regex, line)
        is_join = "added" in line or "joined" in line
        
        if match:
            date_str, time, user, msg = match.groups()
            logs.append({"date": date_str, "user": user, "type": "message"})
            if user not in user_days: user_days[user] = set()
            user_days[user].add(date_str)
        elif is_join and "," in line:
            date_str = line.split(',')[0]
            # FIXED: Changed .push to .append
            logs.append({"date": date_str, "type": "join"})

    # Get unique dates and sort them
    unique_dates = list(set(l["date"] for l in logs if "/" in l["date"]))
    unique_dates.sort(key=lambda x: datetime.strptime(x, '%m/%d/%y'))
    
    last_7_days = unique_dates[-7:]

    chart_data = []
    for d in last_7_days:
        active_users = len(set(l["user"] for l in logs if l["date"] == d and l["type"] == "message"))
        new_joins = len([l for l in logs if l["date"] == d and l["type"] == "join"])
        chart_data.append({"date": d, "activeUsers": active_users, "newJoins": new_joins})

    power_users = [u for u, days in user_days.items() if len([d for d in days if d in last_7_days]) >= 4]

    return {"chartData": chart_data, "powerUsers": power_users}