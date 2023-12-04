# Reference: https://github.com/ra002890/blind_sql_injection_dns/blob/main/site/main.py
# Date: Oct 21, 2022

@app.middleware("http")
async def show_cookie(request: Request, call_next):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId")) if request.cookies.get("TrackingId") else None
    print(tracking_id)
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId")) if request.cookies.get("TrackingId") else None
    
    _response = templates.TemplateResponse("home.html", {"request": request})
    if not tracking_id:
        _response.set_cookie(key='TrackingId', value=base64_encode_str(str(uuid4())))
    else:
        _response = try_direct_login(tracking_id, request=request)
    return _response

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, uname: str = Form(), psw: str = Form()):
    tracking_id = base64_decode_str(request.cookies.get("TrackingId"))
    user = database.login(uname, psw)
    if user:
        database.save_trackid(trackid=tracking_id, userid=user[0])
        _response = templates.TemplateResponse("main.html", {"request": request, "user": user[1]})
    else:
        _response = templates.TemplateResponse("home.html", {"request": request, "error": "Invalid user credentials"})
    return _response

def try_direct_login(trackid, request):
    user = database.try_direct_login(trackid)
    if user:
        return templates.TemplateResponse("main.html", {"request": request, "user": user[1]})
    else:
        return templates.TemplateResponse("home.html", {"request": request})

def base64_encode_str(str):
    str_bytes = str.encode("ascii")
    base64_bytes = base64.b64encode(str_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def base64_decode_str(str):
    base64_bytes = str.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string