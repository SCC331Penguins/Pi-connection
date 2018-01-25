import requests
import wifi

# get self ip
# connect to router
# connect to PHOTON-


def send_post():
    url = 'http://192.168.0.1/wifi'  # Set destination URL here
    ssid = "pi"
    password = "pass"
    ip = "0.0.0.0"
    post_fields = ssid + "\t" + password + "\t" + ip  # Set POST fields here
    try:
        r = requests.post(url, post_fields)
    except requests.exceptions.ConnectionError:
        print("failed")
        r.status_code = "Connection refused"

    print("here")

    print(r.content)

    print(r.text)  # get text sent

    r.status_code  # get response


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
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell

    return False

if __name__ == '__main__':
    # Search WiFi and return WiFi list
    print(Search())

    # Connect WiFi with password & without password
    print(Connect('ClosedWiFi', 'password'))

    # Delete WiFi from auto connect list
    print(Delete('DeleteWiFi'))
