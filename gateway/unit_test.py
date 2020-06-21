import pytest
import gateway
from gateway import generate_payload, get_reply

command_prefix = gateway.client.command_prefix

@pytest.mark.asyncio
async def test_genpay_blank():
    """Tests that blank inputs don't yield anything""" 
    assert await generate_payload("") == None
    assert await generate_payload(" ") == None
    assert await generate_payload(None) == None
    assert await generate_payload(dict()) == None 


@pytest.mark.asyncio
async def test_genpay_noargs():
    """Tests that commands with no arguments are accepted correctly"""
    res = await generate_payload(command_prefix + "cmd")
    assert res["command"] == "cmd"
    res = await generate_payload(command_prefix + "cmd ")
    assert res["command"] == "cmd"
    res = await generate_payload(command_prefix + "cmd        ")
    assert res["command"] == "cmd"


@pytest.mark.asyncio
async def test_genpay_bad_prefix():
    """Tests that bad command prefixes are rejected"""
    bad_prefix = "/" if command_prefix != "/" else "."
    assert await generate_payload(bad_prefix) == None
    assert await generate_payload(bad_prefix + "cmd") == None


@pytest.mark.asyncio
async def test_genpay_args():
    """Tests that arguments are parsed correctly"""
    res = await generate_payload(command_prefix + "cmd arg1 arg2 arg3")
    assert len(res["arguments"]) == 3
    assert res["arguments"][0] == "arg1"
    assert res["arguments"][1] == "arg2"
    assert res["arguments"][2] == "arg3"

    res = await generate_payload(command_prefix + "cmd arg1 'arg2 arg3' arg4")
    assert len(res["arguments"]) == 3
    assert res["arguments"][0] == "arg1"
    assert res["arguments"][1] == "arg2 arg3"
    assert res["arguments"][2] == "arg4"    
