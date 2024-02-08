# -*- coding: utf-8 -*-
"""
Created on Feb 08 05:03:24 2024

@author: Jerome Yutai Shen

"""
import pytest
from atm_transictions import main


class TestMain:

    def test_demo1(self, monkeypatch):
        inputs = iter(["hacker",
                       "10",
                       "8",
                       "withdraw 5",
                       "login foo",
                       "login hacker",
                       "withdraw 15",
                       "deposit 20",
                       "withdraw 15",
                       "balance",
                       "logout"])
        monkeypatch.setattr('builtins.input', lambda : next(inputs))
        result = main()
        assert result == ["Success=False unauthorized",
                          "Success=False unauthorized",
                          "Success=True authorized",
                          "Success=False authorized",
                          "Success=True authorized",
                          "Success=True authorized",
                          "Success=True authorized 15",
                          "Success=True unauthorized"]

    def test_demo2(self, monkeypatch):
        inputs = iter(["somepass",
                       "100",
                       "5",
                       "logout",
                       "login somepass",
                       "balance",
                       "login somepass",
                       "login wrongpass"])
        monkeypatch.setattr('builtins.input', lambda : next(inputs))
        result = main()
        assert result == ["Success=False unauthorized",
                          "Success=True authorized",
                          "Success=True authorized 100",
                          "Success=False authorized",
                          "Success=False authorized"]


if __name__ == "__main__":
    pytest.main(["-v"])

