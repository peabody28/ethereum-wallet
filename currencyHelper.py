wei_to_ether_coef = 10**18

def toEther(weiValue):
    return weiValue / wei_to_ether_coef

def toWei(etherValue):
    return int(etherValue * wei_to_ether_coef)