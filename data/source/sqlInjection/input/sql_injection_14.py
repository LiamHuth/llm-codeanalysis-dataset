#
#

@app.route('/init')
def init():
    db.drop_all()
    db.create_all()
    print("Finished Database Reset")
    return redirect("/")
    
@app.route("/comment", methods=["POST"])
def postComment():
    comment = request.form['comment']
    query = "INSERT INTO comments (comment) VALUES ('" + comment + "');"
    print(query)
    connection = engine.connect()
    result = connection.execute("INSERT INTO comments (comment) VALUES ('" + comment + "');")
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def hello():
    comments = Comment.query.all()
    completeString = ""
    for c in comments:
        commentString = "<p>Comment: " + c.comment + "</p>"
        completeString += commentString
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Comments</h1>
        %s
        <form method="POST" action="/comment">
            <textarea name="comment" style="width: 300px; height: 150px;" placeholder="comment"></textarea>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """ %(completeString)
