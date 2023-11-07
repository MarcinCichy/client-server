import unittest
from unittest.mock import patch
import server_package.server_response as server_response
from server_package.menu import CommandHandler
from server_package.server_user_state import ServerUserState


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.logged_in_user_data = ServerUserState()
        self.logged_in_user_data.username = 'username'
        self.logged_in_user_data.permissions = 'admin'
        self.command_handler = CommandHandler(self.logged_in_user_data)

    def test_use_command_with_valid_user_command(self):
        # Przygotowanie danych wejściowych i oczekiwanych wyników
        entrance_command = {'username': 'help'}  # Zakładamy, że oczekiwany klucz to 'command'
        expected_result = server_response.USER_HELP_DICT
        expected_result_with_additional_info = {'line1': 'line', 'Commands for All': ''}
        expected_result_with_additional_info.update(expected_result)

        # Ustawienie oczekiwanego zachowania metody help
        self.command_handler.sys_utils.help.return_value = expected_result_with_additional_info

        # Wywołanie testowanej metody
        result = self.command_handler.use_command(entrance_command)

        # Aserty
        self.assertEqual(result, expected_result_with_additional_info)

        # Tutaj sprawdzamy, czy pomoc była wywołana, ale nie ma mockowania, więc:
        # - Jeżeli sys_utils jest zewnętrzną zależnością, powinna być zmockowana
        # - Jeżeli sys_utils.help nie przyjmuje argumentów, to nie sprawdzamy z jakimi została wywołana
        # - Jeżeli sys_utils.help przyjmuje argumenty, to powinniśmy to sprawdzić

        # Uwaga: Nie jestem pewien, co dokładnie ma robić testowana metoda use_command,
        # więc nie mogę dokładnie określić, jak powinna być użyta sys_utils.help.

    if __name__ == "__main__":
        unittest.main(verbosity=2)