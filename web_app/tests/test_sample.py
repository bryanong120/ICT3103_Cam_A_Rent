from os import lseek
import pytest
from flask import Flask, session

# def test_request_example(client):
#     response = client.get("/test")
#     assert b"I am connected to db!" in response.data

def test_access_session(client):
    with client:
        client.post("/user/login/", data = {
            "email": "2001011@sit.singaporetech.edu.sg",
            "password" : "Runescape@2007"})

        assert session["user"]["email"] == "2001011@sit.singaporetech.edu.sg"
            
