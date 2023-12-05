#
#

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