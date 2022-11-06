# otpverify.py
import os
from flask import current_app
from twilio.rest import Client, TwilioException


def getVerifyAPI():
    return Client(os.getenv('TWILIO_SSID'),os.getenv('TWILIO_TOKEN')).verify.services(os.getenv('VERIFY_SSID'))

def requestPhoneOTP(phone):
    verify = getVerifyAPI()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException:
        
        return "OTP request limit reached, please try again in 10 minutes"

def checkPhoneOTP(phone, token):
    verify = getVerifyAPI()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'
    
def requestEmailOTP(email):
    verify = getVerifyAPI()
    try:
        verify.verifications.create(to=email, channel='email')
    except TwilioException:
        return "OTP request limit reached, please try again in 10 minutes"

def checkEmailOTP(email, token):
    verify = getVerifyAPI()
    try:
        result = verify.verification_checks.create(to=email, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'