from flask import Flask,render_template, request

def subnet(sub):

    lev = ''

    def bin_to_deci(x,n):
        k = 0
        dec = 0
        for i in n:
            if k < x:
                dec += int(i) * 2**k
                k += 1
        return dec

    def bin_deci(x,n):
        dec = 0
        for i in n:
            if x > -1:
                dec += int(i) * 2**x
                x -= 1 
        return dec

    ip = sub.split('/')
    ip_l = ip[0].split('.')
    cidr = ip[1]
    if int(cidr) == 32:
        print(f'IP Address:{ip[0]}\nNetwork Address:{ip[0]}\nUsable Host IP Range:NA\nBroadcast Address:{ip[0]}\nTotal Number of Hosts:1\nNumber of Usable Hosts:0\nSubnet Mask:255.255.255.255\nWildcard Mask:	0.0.0.0\nBinary Subnet Mask:11111111.11111111.11111111.11111111\nIP Class:	C\nIP Type:	Public\n')
        del ip
    else:
        if len(ip_l) == 4 : 
            if int(cidr) < 33 and int(cidr) > 7:
                if int(cidr) < 16 :
                    ip_cat = 'A'
                elif int(cidr) < 24 :
                    ip_cat = 'B'
                else:
                    ip_cat = 'C'

                binary_bits = '.'.join([''.join('1' if j < int(cidr) else '0' for j in range(i,i+8)) for i in range (0,32,8)])
                subnetmask = '.'.join(str(bin_to_deci(len(i),i[::-1])) for i in binary_bits.split('.'))
                msb = 2 ** (int(cidr) % 8)
                ip_class = ('Classful' if msb == 1 else 'Classless')
                uhost = (2 ** (32 - int(cidr))) - 2
                wildcardmask = '.'.join(str(255-int(i)) for i in subnetmask.split('.'))
                for x,y in zip(subnetmask.split('.'),range(1,5)):
                    if int(x) != 255:
                        editableoctet = y - 1
                        break
                
                #last_bit = bin(int(ip_l[editableoctet]))[2:]
                #last_bit2 = last_bit
                #last_bit = ('.'.join('0' for i in range(8-len(last_bit2))) + last_bit2)[:int(8-msb)]

                lev += (f'\nSubnetmask : {subnetmask} \nPossilble networks : {msb} \nUsable Host for each subnet : {uhost} \nBinary Bits : {binary_bits}\nWildcard mask : {wildcardmask}\nClass:{ip_cat}-{ip_class}\n')
                start_nw_id = 0
                host_start_ip = 0
                x = '.'.join(ip_l[i] for i in range(editableoctet))
                lev += ('-----------------------------------------------------------------\n|Network ID     |          Host IP range        |    Boardcast  |\n-----------------------------------------------------------------\n')
                for y in range(msb):
                    if int(cidr) > 7 and int(cidr) < 16 :
                        rangenid = [str(x+'.'+str(start_nw_id)+'.'+'0.'+str(host_start_ip)),str(x+'.'+str(start_nw_id)+'.'+'0.'+str(host_start_ip+1))]
                    elif int(cidr) >= 16 and int(cidr) < 24:
                        rangenid = [str(x+'.'+str(start_nw_id)+'.'+str(host_start_ip)),str(x+'.'+str(start_nw_id)+'.'+str(host_start_ip+1))]
                    elif int(cidr) >= 24 and int(cidr) < 32:
                        rangenid = [str(x+'.'+str(start_nw_id)),str(x+'.'+str(start_nw_id))]
                    else:
                        rangenid = [str(x+'.'+str(start_nw_id)),str(x+'.'+str(start_nw_id))]

                    mid_cast = [int(x)+int(y) for x,y in zip(rangenid[0].split('.'),wildcardmask.split('.'))]
                    end_range_host = '.'.join(str(i) if k != 3 else str(i-1) for i,k in zip(mid_cast,range(len(mid_cast))))
                    start_nw_id += int(256/msb)
                    bb_cast = '.'.join(str(i) for i in mid_cast)

                    lev += (f'|{rangenid[0].center(15)}|{rangenid[1].center(15)}-{end_range_host.center(15)}|{bb_cast.center(15)}|\n')
    return lev

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results',methods=['GET','POST'])
def results():
    if request.method == 'POST':
        ip = request.form['textinput']
        res = subnet(ip)
        splited_res = res.replace('\n','<br>')
    return render_template('results.html',output = splited_res,ipwcidr = ip)

if __name__ == '__main__':
    app.run(host='https://ipflask-production.up.railway.app/',debug=True,port=443)