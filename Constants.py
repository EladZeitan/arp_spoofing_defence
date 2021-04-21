from util.UtilConstants import UtilConstants
import data_base_lib
import os
from pathlib import Path


def create_db_table(file_name, table_name, columns: tuple):
    ATTACKS_DATA = data_base_lib.DataBaseTable(file_name, table_name,
                                               (('attacker_mac', 'text'), ('date', 'text')))


def get_file_location(name: str, to_format='.png', path=str(str(Path.cwd()))) -> str:
    """
    A util function for helping in the path naming process.
    :param name: The name of the file.
    :param to_format: The format of the file. Default is PNG
    :param path: The abs path of the file. Default is under .../res/des/
    :return: The full abs path of the file.
    """
    f = name + to_format
    return os.path.join(path, f)


class Images:
    KV_FILE = get_file_location('System_View', to_format='.kv')
    MAIN_SCREEN = get_file_location('main_screen')
    ATTACKS_LOG_SCREEN = get_file_location('attacks_log_screen')

    VIEW_ATTACKS_BUTTON = get_file_location('view_attacks_button')
    BACK_BUTTON = get_file_location('back_button')


class ClientConstants:

    # Socket Params:
    PORT = 10

    # Addresses:
    ATTACKER_MAC_ADDRESS = ''
    SOCKET_ADDRESS = ()
    ROUTER_IP = ''
    CLIENT_IP = ''

    # Messages:
    # format: attacker mac address
    REPORT_MESSAGE = 'REP' + UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS

    # format: router ip, mac address
    SIGN_UP_MESSAGE = 'NEW' + UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS + \
                      UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS

    # DataBase:
    ATTACKS_DATA = data_base_lib.DataBaseTable('attacks.db', 'attacks',
                                               (('attacker_mac', 'text'), ('date', 'text')))
    ATTACKS_DATA.build_table()


    # OtherParams:
    FOUND_ATTACK = False
    ID = ()
    CACHE = {}


class ServerConstants:

    # Messages:
    REGISTRATION_COMPLETE_MESSAGE = 'OK'
    ALERT_MESSAGE = 'ALERT' + UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS + \
                    UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS
    WARNING_MESSAGE = 'WARN' + UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS + \
                      UtilConstants.DATA_SEPARATOR + UtilConstants.FORMAT_BRACKETS
    BLOCK_MESSAGE = 'BLOCK'
    # CLIENT_ID_MESSAGE = 'ID' + SEPARATOR + FORMAT_BRACKETS + SEPARATOR + FORMAT_BRACKETS

    # Addresses:
    ADDRESS = ('0.0.0.0', 10)

    # DataBase:
    CLIENT_DATA_COLUMNS = (('router_ip', 'text'), ('client_ip', 'text'),
                           ('client_mac', 'text'), ('is_attacked', 'integer'))

    CLIENTS_DATA = data_base_lib.DataBaseTable('server_data.db', 'clients',
                                               CLIENT_DATA_COLUMNS)
    CLIENTS_DATA.build_table()

    ATTACK_DATA_COLUMN = (('router_ip', 'integer'), ('data', 'text'), ('attacker_mac', 'text'))
    ATTACK_DATA = data_base_lib.DataBaseTable('server_data.db', 'attacks', ATTACK_DATA_COLUMN)
    ATTACK_DATA.build_table()

    # CLIENTS_DATA = data_base_lib.DataBaseTable('server_data.db', 'clients',
    #                                           (('group_id', 'integer'), ('self_id', 'integer'),
    #                                         ('router_ip', 'text'), ('client_ip', 'text'), ('is_attacked', 'integer')))
    # ATTACK_DATA = data_base_lib.DataBaseTable('server_data.db', 'attacks',
    #                                          (('group_id', 'integer'), ('data', 'text'), ('attacker_mac', 'text')))

    # Others:
    MAX_WARNINGS = 5

