from oath import totp, accept_totp
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage:"
        print "check_auth.py [secret] [code_from_authenticator]"
        sys.exit(1)

    secret = sys.argv[1]
    code = sys.argv[2]

    print accept_totp(code, secret, "dec6")