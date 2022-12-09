def subnet(sub,cidr):
    networkid = ['Network ID']
    netrange = ['Usable Host IP Range']
    broadcastip = ['Broardcast IP']

    if sub.split('.')[0] == '10' or sub.split('.')[0] == '172' or sub.split('.')[0] == '192':
        ip_type = 'Private'
    else:
        ip_type = 'Public' 
    ipdict = {}
    
    ipdict.update({'IP Address':sub})
    ipdict.update({'CIDR':cidr})
    if int(ipdict.get("CIDR")) == 32 and len(sub.split('.')) == 4:
        output += (f'IP Address:{ipdict.get("IP Address")}\nNetwork Address:{ipdict.get("IP Address")}\n[netid]\nUsable Host IP Range:NA\nBroadcast Address:{ipdict.get("IP Address")}\nTotal Number of Hosts:1\nNumber of Usable Hosts:0\nSubnet Mask:255.255.255.255\nWildcard Mask: 0.0.0.0\nBinary Subnet Mask:11111111.11111111.11111111.11111111\nIP Class:	C\nIP Type:	Network IP\n')
    elif len(sub.split('.')) == 4:
        if int(ipdict.get("CIDR")) < 33 and int(ipdict.get("CIDR")) > 0:
            if 7 < int(ipdict.get("CIDR")) < 16 :
                ipdict.update({"ip_cat" : 'A'})
                ipdict.update({"editableoctet": 1})
            elif 15 < int(ipdict.get("CIDR")) < 24 :
                ipdict.update({"ip_cat" : 'B'})
                ipdict.update({"editableoctet": 2})
            elif 23 < int(ipdict.get("CIDR")) < 32:
                ipdict.update({"ip_cat" : 'C'})
                ipdict.update({"editableoctet": 3})
            else:
                ipdict.update({"ip_cat" : 'Any  '})
                ipdict.update({"editableoctet": 0})

            ipdict.update({"binary_bits" : '.'.join([''.join('1' if j < int(ipdict.get("CIDR")) else '0' for j in range(i,i+8)) for i in range (0,32,8)])})
            ipdict.update({"subnetmask" : '.'.join(str(int(j,2)) for j in ipdict.get("binary_bits").split('.'))})
            ipdict.update({"MSB" : 2 ** (int(ipdict.get("CIDR")) % 8)})
            ipdict.update({'ip_class':'Classful'}) if ipdict.get("MSB") == 1 else ipdict.update({'ip_class':'Classless'})
            ipdict.update({"uhost":(2 ** (32 - int(ipdict.get("CIDR")))) - 2})
            ipdict.update({"wildcardmask":'.'.join(str(255-int(i)) for i in ipdict.get("subnetmask").split('.'))})
            bid = ''.join(bin(int(i))[2:].zfill(8) for i in sub.split('.'))
            intid = int(bid,2)

        start_nw_id = 0
        host_start_ip = 0
        x = '.'.join(ipdict.get("IP Address").split('.')[i] for i in range(ipdict.get("editableoctet")))
        output = (f'IP Address:{ipdict.get("IP Address")}\nCIDR:{ipdict.get("CIDR")}\n[netid]\nSubnetmask : {ipdict.get("subnetmask")} \nPossilble networks : {ipdict.get("MSB")} \nUsable Host for each subnet : {ipdict.get("uhost")} \nBinary Bits : {ipdict.get("binary_bits")}\nWildcard mask : {ipdict.get("wildcardmask")}\nClass:{ipdict.get("ip_cat")}-{ipdict.get("ip_class")}\nIP Type:{ip_type}')
        output += f'\nBinary ID:{bid}\nInteger ID:{intid}\nHex ID:{hex(intid)}\nin-addr.arpa:{".".join(sub.split(".")[i] for i in range(3,-1,-1))}.in-addr.arpa'
        #output += ('[Begin]\n-----------------------------------------------------------------\n|   Network ID  |          Host IP range        |    Broadcast  |\n-----------------------------------------------------------------')
        for y in range(ipdict.get("MSB")):
            if int(ipdict.get("CIDR")) > 7 and int(ipdict.get("CIDR")) < 16 :
                rangenid = [str(x+'.'+str(start_nw_id)+'.'+'0.'+str(host_start_ip)),str(x+'.'+str(start_nw_id)+'.'+'0.'+str(host_start_ip+1))]
            elif int(ipdict.get("CIDR")) >= 16 and int(ipdict.get("CIDR")) < 24:
                rangenid = [str(x+'.'+str(start_nw_id)+'.'+str(host_start_ip)),str(x+'.'+str(start_nw_id)+'.'+str(host_start_ip+1))]
            elif int(ipdict.get("CIDR")) >= 24 and int(ipdict.get("CIDR")) < 32:
                rangenid = [str(x+'.'+str(start_nw_id)),str(x+'.'+str(start_nw_id+1))]
            else:
                rangenid = [str(str(start_nw_id)+'.0.0.0'),str(str(start_nw_id)+'.0.0.1')]
            mid_cast = [int(x)+int(y) for x,y in zip(rangenid[0].split('.'),ipdict.get('wildcardmask').split('.'))]
            end_range_host = '.'.join(str(i) if k != 3 else str(i-1) for i,k in zip(mid_cast,range(len(mid_cast))))
            start_nw_id += int(256/ipdict.get("MSB"))
            bb_cast = '.'.join(str(i) for i in mid_cast)
            #output += (f'\n|{rangenid[0]}|{rangenid[1]}-{end_range_host}|{bb_cast}|')
            networkid.append(rangenid[0])
            netrange.append(f'{rangenid[1]}-{end_range_host}')
            broadcastip.append(bb_cast)
            if end_range_host == '122.0.0.254':
                pass
            if sub == rangenid[0] or sub == end_range_host or sub == rangenid[1] or sub == bb_cast:
                repplace = (f'Network ID:{rangenid[0]}\nHost Range:N/A\nBroadcast Address:{bb_cast}')
                output = output.replace('[netid]',repplace)
            elif int(rangenid[1].split('.')[ipdict.get("editableoctet")]) <= int(sub.split('.')[ipdict.get("editableoctet")]) <= int(end_range_host.split('.')[ipdict.get("editableoctet")]) :
                repplace = f'Network ID:{rangenid[0]}\nHost Range:{rangenid[1]}-{end_range_host}\nBroadcast Address:{bb_cast}'
                output = output.replace('[netid]',repplace)

    return [output,networkid,netrange,broadcastip]