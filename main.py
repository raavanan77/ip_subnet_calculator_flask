from flask import Flask, request,render_template
import os
from ip_subnet_calc import subnet
import jinja2

env = jinja2.Environment()
env.globals.update(zip=zip)

app = Flask(__name__)

def validate(sub,cidr):
    output = ''
    count = 0
    ip = sub.split('.')
    if len(ip) == 4 and 0 < int(cidr) <= 32 and ip[0].isdigit():
        for i in range(0,4):
            if -1 < int(ip[i]) < 256:
                count += 1
            if count == 4:
                del count
                return True
        else:
            output += ("Entered IP or CIDR is in wrong fromat please enter again")
            return output
    else:
        output += ("Entered IP or CIDR is in wrong fromat please enter again")
        return output


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        ip = (request.form['textinput']).split('/') 
        if 1 < len(ip) < 3 :
            valid = validate(ip[0],ip[1])
            if valid == True:
                res = subnet(ip[0],ip[1])
                #res = res.split('[Begin]')
                return render_template('home.html',output = res[0].split('\n'), ziploop =  zip(res[1],res[2],res[3]),v='',sv='hidden')
            else:
                return render_template('home.html',serious = valid,sv='')
        else:
            return render_template('home.html',serious = 'You typed nothing',sv='')
    else:
        return render_template('home.html',v='hidden')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
