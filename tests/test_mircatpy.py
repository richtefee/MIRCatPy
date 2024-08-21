from mircatpy import MIRcat

mc = MIRcat()

mc.connect()

mc.display_status()

mc.tune('wl',7)

mc.display_status()

mc.tune('wl',7.1)

mc.display_status()

mc.tune('wn',1400)

mc.display_status()