from os import lseek
from queue import Empty
from urllib import response
import pytest
from flask import Flask, session, url_for

# def test_request_example(client):
#     response = client.get("/test")
#     assert b"I am connected to db!" in response.data

def tests(client):
    with client:
        client.post("/user/login/", data = {
            "email": "2001011@sit.singaporetech.edu.sg",
            "password" : "P@ssw0rd1",})
        
        #Check if login works
        assert session['logged_in'] == True

        #Check if session information is correct
        assert session["user"]["email"] == "2001011@sit.singaporetech.edu.sg"

        #Check logout
        client.get('/user/signout/')
        assert len(session) == 0