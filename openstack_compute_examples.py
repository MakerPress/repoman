from openstack.compute import Compute
compute = Compute(username="makerpressadmin", apikey="39a15325f2e67a3ff68d59b76f990616")

# List all available flavors
#flv = compute.images.list()  #Lists available image
#img = compute.flavors.list()  #lists available flavors

#Grab a particular image
im = compute.images.find(name="Ubuntu 10.10 (maverick)")
fl = compute.flavors.find(name="256 server")


# To create a new server
s = compute.servers.create("fred", image=im, flavor=fl)

# get login information:
# s.adminPass
# s.public_ip


# to add files to the server, create a dictionary like this:
fileInfo = {'/root/test2.txt': 'hello again', '/root/test.txt': 'hello there andrew!!!'}
s = compute.servers.create("gold", image=im, flavor=fl, files=fileInfo)


# To add a public key to the authorized login and main git repo:

# pkInfo = { 
   '/root/.ssh/authorized_keys2' : 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3A9wtS2JA/RhgKyBU+inwBWo/33YU1yMLjb1lpBKBm+uX0ilBZVN0bpOk7vPP8SGxo5q8UjcoXNDplC4hOsxAJTqOoTvW4R5xj+Cry8QK2WIqs/j6+nJlD1EaNI8DEPl9fBXNtTKr+lkguN0UGKU/GNrtyt8SrngfFkK5JpzxbsCRp8Sx/9gO6j96jHutzccPvpOs260bJ8btZcmmHhacgurVdu9E5rmbO20Kzsnb8S0z24NZnfyBsExt+UqzVKgSZSPzvRrdYVg+5T9UK6zEO7B7DgrW+ixujW24KlaNfNiCCyiE1EgyVQb3vxV/8iGJTh9EQ0ODbh3HRFIKIC9hw== odewahn@MacOdewahn.home',
   '/home/git/.ssh/authorized_keys2': 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3A9wtS2JA/RhgKyBU+inwBWo/33YU1yMLjb1lpBKBm+uX0ilBZVN0bpOk7vPP8SGxo5q8UjcoXNDplC4hOsxAJTqOoTvW4R5xj+Cry8QK2WIqs/j6+nJlD1EaNI8DEPl9fBXNtTKr+lkguN0UGKU/GNrtyt8SrngfFkK5JpzxbsCRp8Sx/9gO6j96jHutzccPvpOs260bJ8btZcmmHhacgurVdu9E5rmbO20Kzsnb8S0z24NZnfyBsExt+UqzVKgSZSPzvRrdYVg+5T9UK6zEO7B7DgrW+ixujW24KlaNfNiCCyiE1EgyVQb3vxV/8iGJTh9EQ0ODbh3HRFIKIC9hw== odewahn@MacOdewahn.home',
'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAuhlfACrZ2zLQHetJL+0r7DWDV/HfE4bHT3NfBLF6wgQuQiQqjhwrECOX2SXp21OyySe27Jh5zPItidxGPPopxq+rJalaFv7ukqXi26k7BBiyxmaokN66jNS//S4eM748pL9cDnoJZtkkbo2fFEczhBNgZzXsq0dDYXDKSBlMwu3Bw1sRIOQK32lIyHGjs/96YzHyyjG+2sS87sInK3YTKwgVAYk5mERGJWSpJWCWXGrKgGkskbii6OLR6bIgiSaIrgYuNnGAHECtJv/h+Dai1ZIPtwRtm9wqGw90Y6Q502NP/nv/Oy9awnphM3MoLJ1gqe+y113dTTONV6qlOppIRQ== mrosedale@dhcp-245-30.east.ora.com'}

# s = compute.servers.create("python-biblio", image=im, flavor=fl, files=pkInfo)



# You can then log in using:
#ssh root@<s.public_id>
#Password is s.adminPass


# To grab a link to a server
#s = compute.servers.find(name="fred")


# To delete a server
# First, grab a reference, and then use
# s.delete()




