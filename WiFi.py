import wifi

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
    print("Connecting")
    cell = FindFromSearchList(ssid)
    if cell:
        savedcell = FindFromSavedList(cell.ssid)
        if cell.encrypted:
            if password != None:
                scheme = Add(cell, password)
                try:                    print(scheme.activate())
                # Wrong Password
                except Exception as e:
                    print(e)
                    print(ssid)
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
    print("saved")
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
    print(Search())
    print(Connect("SCC33X_2", "!studio?x57"))