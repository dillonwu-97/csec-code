from encryption import RSA, bytes_to_long
# from secret import FLAG
FLAG = 'helloworld'
import socketserver
import signal


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        signal.alarm(0)
        main(self.request)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def sendMessage(s, msg):
    s.send(msg.encode())


def recieveMessage(s, msg):
    sendMessage(s, msg)
    return s.recv(4096).decode().strip()


def parseEmail():
    with open("email.txt", "r") as f:
        data = f.readlines()
    user = data[0].strip()[len("From: "):]
    return user.encode(), "".join(data)

# Generate some header and some signature 
def generateHeaders(rsa, signature):
    signature = f"signature: {signature.hex()}\n"
    certificate = f"certificate: \n{rsa.export_key()}\n"
    return signature + certificate

# make sure that the forged signature is not some trivial case?
def different(rsa, signature, forged_signature):
    signature = bytes_to_long(signature)
    forged_signature = bytes_to_long(forged_signature)
    if ((forged_signature % rsa.n) != signature):
        return True
    return False


def main(s):
    rsa = RSA(2048)

    user, data = parseEmail()
    print(user)
    print("---" * 10)
    print(data)

    signature = rsa.sign(user)
    rsa.verify(user, signature)

    headers = generateHeaders(rsa, signature)

    valid_email = headers + data
    sendMessage(s, valid_email + "\n\n")

    # The goal is to forge a signature?
    # Maybe add a bit of extra padding can work?
    print("Beginning try except")
    try:
        forged_signature = recieveMessage(s, "Enter the signature as hex: ")
        print(forged_signature)
        forged_signature = bytes.fromhex(forged_signature)
        print("forged: ", forged_signature)

        if not rsa.verify(user, forged_signature):
            sendMessage(s, "Invalid signature")

        if different(rsa, signature, forged_signature):
            sendMessage(s, FLAG)
    except:
        sendMessage(s, "An error occured")


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1338), Handler)
    server.serve_forever()
