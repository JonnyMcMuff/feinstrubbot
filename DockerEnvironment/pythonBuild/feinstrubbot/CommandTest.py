import unittest
from unittest.mock import MagicMock

from feinstrubbot.CreateUserCommand import CreateUserCommand


class TestCreateUserCommand(unittest.TestCase):
    def test_execute_success(self):
        usersMock = MagicMock()
        command = CreateUserCommand(usersMock, 1, "Nils", "Maichingen", 42, 1337, 2)
        command.execute()
        usersMock.insert_one.assert_called()


if __name__ == '__main__':
    unittest.main()
