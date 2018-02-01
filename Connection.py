import time
import requests
import wifi
import socket

# get self ip
# connect to router
# connect to PHOTON-
foreignPhotons = []
urlPhoton = 'http://192.168.0.1/wifi'  # Set destination URL here
ssidRouter = "SCC33X_1"
passwordRouter = "!studio?x47"
ipRouter = "192.168.0.104"
#ipRouter = socket.gethostbyname(socket.gethostname())
print("Router IP: ")
print(ipRouter)


def send_post(photonssid):
    post_fields = ssidRouter + "\t" + passwordRouter + "\t" + ipRouter  # Set POST fields here
    try:
        r = requests.post(urlPhoton, post_fields)
        if(r.status_code):
            print("Response code: ")
            print(r.status_code)  # get response
        if (r.status_code == 404):
            foreignPhotons.append(photonssid)
    except requests.exceptions.ConnectionError:
        print("failed")
    


def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)

    return wifilist


def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False


def Connect(ssid, password=None):
    print("Connecting to")
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)
        if cell.encrypted:
            if password != None:
                scheme = Add(cell, password)
                try:
                    print(scheme.activate())
                # Wrong Password
                except Exception as e:
                    print(e)
                    #Delete(ssid)
                    return False
                return cell
            else:
                return False
        else:
            scheme = Add(cell)
            try:
                scheme.activate()
            except Exception as e:
                print(e)
                return False
            return cell
    return False


def Add(cell, password=None):
    if not cell:
        return False
    print(cell)
    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    print(scheme)
    try:
        scheme.save()
    except Exception as e:
        print(e)
    return scheme


def Delete(ssid):
    if not ssid:
        return False
    cell = FindFromSavedList(ssid)
    if cell:
        cell.delete()
        return True

    return False


if __name__ == '__main__':
    # Search WiFi and return WiFi list
    while True:
        cells = Search()
        print("----------------")
        for cell in cells:
            print(cell)
            y = cell.ssid.encode("ascii")
            if y.startswith("Photon-" ) and not y in foreignPhotons:
                print(Connect(y))
                send_post(y)
        time.sleep(30)