#
#

import request

@app.route("/register", methods=['POST', 'GET'])
def sessions_register():
    if request.method == 'POST':
        # check if data already exists.
        username = request.form['username']
        password = request.form['password']
        if request.form['username'] =='' or request.form['password'] =='':
            return redirect(url_for('login'))
        else:
            if not mydata.login_checker_safe(username, password):
                mydata.register(escape(username), escape(password))
                return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
