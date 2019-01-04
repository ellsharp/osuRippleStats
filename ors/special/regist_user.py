import sys
from ors.script import converter
from ors.script import database
from ors.script import util

# CHUDAN #
if __name__ == "__main__":
    from ors.special.regist_user import RegistUser
    RegistUser().execute(sys.argv[1:])

class RegistUser(object):
    def execute(self, user_ids):
        user_ids = [1000]
        for user_id in user_ids:
            print(user_id)
            # Duplicate check.
            result = database.execute_statement('m_users_001', user_id)
            if result[1][0]['count'] == 0:
                # Regist user.
                now = util.datetime_now()
                now = converter.convert_datetime(now)
                result = database.execute_statement('m_users_002', user_id, 1, now)
                print(result)
            else:
                # Nothing to do.

                print('user_id[%s] is already regsistred.')
