import os
from queue import Empty
from urllib import response
import pytest
from flask import Flask, session, url_for
from dotenv import load_dotenv

# def test_request_example(client):
#     response = client.get("/test")
#     assert b"I am connected to db!" in response.data
load_dotenv()

def tests(client):
    with client:
        client.post("/user/login/", data = {
            "email": str(os.getenv('EMAIL_TEST')),
            "password" : os.getenv('PASSWORD_TEST')})
        
        #Check if login works
        assert session['logged_in'] == True

        #Check if session information is correct
        assert session["user"]["email"] == os.getenv('EMAIL_TEST')

        #Check logout
        client.get('/user/signout/')
        assert len(session) == 0