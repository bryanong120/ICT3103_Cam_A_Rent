from os import lseek
import pytest
from flask import Flask

def test_request_example(client):
    response = client.get("/test")
    assert b"I am connected to db!" in response.data
