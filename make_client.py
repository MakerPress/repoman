#!/bin/python
from openstack.compute import Compute

instance_name = "test-rclocal"

#
# Make a list of master keys to install
#
master_key_list = [
"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA3A9wtS2JA/RhgKyBU+inwBWo/33YU1yMLjb1lpBKBm+uX0ilBZVN0bpOk7vPP8SGxo5q8UjcoXNDplC4hOsxAJTqOoTvW4R5xj+Cry8QK2WIqs/j6+nJlD1EaNI8DEPl9fBXNtTKr+lkguN0UGKU/GNrtyt8SrngfFkK5JpzxbsCRp8Sx/9gO6j96jHutzccPvpOs260bJ8btZcmmHhacgurVdu9E5rmbO20Kzsnb8S0z24NZnfyBsExt+UqzVKgSZSPzvRrdYVg+5T9UK6zEO7B7DgrW+ixujW24KlaNfNiCCyiE1EgyVQb3vxV/8iGJTh9EQ0ODbh3HRFIKIC9hw== odewahn@MacOdewahn.home",
"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA1wJrcvsdDaCTRCH3IF6GD6CP78/3SKI1P6xLKs4lU76JNNzSt91KZW0Fp77fGJR/iwsDbgN8+luVLO2GOS8f+fd5y81yeNhUzFZsQ2WV35TCwFU8TSKq7GuoJarRVXBBFg59AwaV07vGH+Tv5J+Eo1F5IUJ6bfn2IjSdXRRhONzk7sn8VMa0Gy14YpP3157MaNLVow6MpozT3e6Pvm1plZYNKjpfjJ2cB+Os8OOEP8m+Y5PG70XyeOPy4eYyBFXezm5rXgoWB7TDUo3XLlnswgwtLhgmEu1aqxqEJ0Dp0H6nMUR+mSCr54Su14P/HNXMsnp2cInKAzTnxAQv3lKTrw== bjepson@Brian-Jepsons-MacBook-Air.local",
"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxb5AGnZxxLpcVHe/TIedf1hRG1FTY4oF2tgM6X6YEY5wk+Di44yxKWcaTorxZuokKV/eNJlhLD+nbrwYlFV6TwPY9UlseD0XsRxyXARH5k8wjZAi69LwVBNm7E6EUc6hog+7w/bVy1OWkAJV8qrJeyh0QJUGCGlW1hBedSDy0huujhWKenltysj8CxiPpCLjgCzeCoc0exbf+YFpuEa0CmFSkc15vMhU/hM1oSaIjpux0AU2HUd0I3Wu7R9StjQEhO0hDdHvcHaW+1dEpSmarD+Eta5rqrEfkXX00xL5juGqaO3+PMj7DvV5+3WbB2lXau3QdZPAqhZ/ExkiBcLPYw== bjepson@Brian-Jepsons-MacBook-Pro.local",
"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxOJb8NPlQ/wD7t/N2U1fo2UjGcn7tew80u/yHHrbSquYh6KoF6BCNRqOuCm9yI+Nva5K65zVXf60+OYWoAIAlsDupZ1JeQEA+T9xuKPr7Cf/h8MCQYSch9KKLzrs3b7lYz2jkCP3drp9q4LUOo3DYKwI6PompqIxuk/V5F1xYRf9BSZ13HXzTgp1GGdqHP0uJTLqdayG8y4UTY7sk6CRs5PO/lsDuqA0SQyFGLHavMBCaeh9YOnqf8BFNCfTv22WHLOGjvPGaLbf+k298BEmYS1lf1R1/IkyDuI5IGxJZMTmxaB1ZX2+n/wtiP2tbcLz8HYnCNsA62V+VuVRYmvX3Q== swallace@oreilly.com"
]


# Now create a compiled version of the master keys
master_key = "\n".join(master_key_list)

# Fix any permssions, ownership, and other issues by setting them in /etc/rc.local
rc_local = """
#!/bin/sh -e
chown git:git /home/git/.ssh/authorized_keys2
exit 0
"""

fileInfo = { 
   '/root/.ssh/authorized_keys2' : master_key,
   '/home/git/.ssh/authorized_keys2': master_key,
   '/etc/rc.local': rc_local
}

#Grab a particular image
compute = Compute(username="makerpressadmin", apikey="39a15325f2e67a3ff68d59b76f990616")
im = compute.images.find(name="client-gold")
fl = compute.flavors.find(name="256 server")
s = compute.servers.create(instance_name, image=im, flavor=fl, files=fileInfo)

#Now print results
print "You can log into this server as root@%s" % s.public_ip




