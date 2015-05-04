import sys
import contextlib
import uuid


from orchestrator.commands.createNewService import main as CreateNewService
from orchestrator.commands.createNewSubService import main as CreateNewSubService
from orchestrator.commands.createNewServiceRole import main as CreateNewServiceRole
from orchestrator.commands.createNewServiceUser import main as CreateNewServiceUser
from orchestrator.commands.assignInheritRoleServiceUser import main as assignInheritRoleServiceUser
from orchestrator.commands.assignRoleSubServiceUser import main as assignRoleSubServiceUser
from orchestrator.commands.assignRoleServiceUser import main as assignRoleServiceUser
from orchestrator.commands.listRoleAssignments import main as listRoleAssignments
from orchestrator.commands.printServices import main as printServices
from orchestrator.commands.printSubServices import main as printSubServices
from orchestrator.commands.printServiceUsers import main as printServiceUsers
from orchestrator.commands.printServiceRoles import main as printServiceRoles


@contextlib.contextmanager
def redirect_argv(args):
    sys._argv = sys.argv[:]
    sys.argv=args
    yield
    sys.argv = sys._argv


class Test_NewService_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["createNewService.py",
                "http",
                "localhost",
                "5000",
                "admin_domain",
                "cloud_admin",
                "password",
                "SmartValencia_%s" % self.suffix,
                "smartvalencia_%s" % self.suffix,
                "adm1_%s" % self.suffix,
                "password",
                "http",
                "localhost",
                "8080"]
        with redirect_argv(args):
            CreateNewService()


class Test_NewSubService_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["createNewSubService.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password",
                "Electricidad_%s" % self.suffix,
                "electricidad_%s" % self.suffix]
        with redirect_argv(args):
            CreateNewSubService()


class Test_NewServiceRole_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["createNewServiceRole.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password",
                "ServiceCustomer_%s" % self.suffix,
                "http",
                "localhost",
                "8080"]
        with redirect_argv(args):
            CreateNewServiceRole()


class Test_NewServiceUser_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["createNewServiceUser.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password",
                "Electricidad",
                "bob_%s" % self.suffix,
                "password"]
        with redirect_argv(args):
            CreateNewServiceUser()


class Test_assignInheritRoleServiceUse_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["assignInheritRoleServiceUser.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password",
                "adm1",
                "SubServiceAdmin"]
        with redirect_argv(args):
            assignInheritRoleServiceUser()


class Test_assignRoleServiceUser_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["assignRoleServiceUser.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password",
                "ServiceCustomer",
                "Carl"]
        with redirect_argv(args):
            assignRoleServiceUser()


class Test_assignRoleSubServiceUser_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["assignRoleSubServiceUser.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "Electricidad",
                "adm1",
                "password",
                "ServiceCustomer",
                "Carl"]
        with redirect_argv(args):
            assignRoleSubServiceUser()


class Test_listRoleAssignments_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["listRoleAssignments.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password"]
        with redirect_argv(args):
            listRoleAssignments()


class Test_printServices_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["printServices.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password"]
        with redirect_argv(args):
            printServices()


class Test_printSubServices_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["printSubServices.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password"]
        with redirect_argv(args):
            printSubServices()


class Test_printServiceUsers_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["printServiceUsers.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password"]
        with redirect_argv(args):
            printServiceUsers()


class Test_printServiceRoles_script(object):
    def __init__(self):
        self.suffix = str(uuid.uuid4())[:8]

    def test(self):
        args = ["printServiceRoles.py",
                "http",
                "localhost",
                "5000",
                "SmartValencia",
                "adm1",
                "password"]
        with redirect_argv(args):
            printServiceUsers()


if __name__ == '__main__':
    test_NewService = Test_NewService_script()
    test_NewService.test()

    test_NewSubService = Test_NewSubService_script()
    test_NewSubService.test()

    test_NewServiceRole = Test_NewServiceRole_script()
    test_NewServiceRole.test()

    test_NewServiceUser = Test_NewServiceUser_script()
    test_NewServiceUser.test()

    test_assignInheritRoleServiceUse = Test_assignInheritRoleServiceUse_script()
    test_assignInheritRoleServiceUse.test()

    test_assignRoleServiceUser = Test_assignRoleServiceUser_script()
    test_assignRoleServiceUser.test()

    test_assignRoleSubServiceUser = Test_assignRoleSubServiceUser_script()
    test_assignRoleSubServiceUser.test()

    test_listRoleAssignments = Test_listRoleAssignments_script()
    test_listRoleAssignments.test()

    test_printServices = Test_printServices_script()
    test_printServices.test()

    test_printSubServices = Test_printSubServices_script()
    test_printSubServices.test()

    test_printServiceUsers = Test_printServiceUsers_script()
    test_printServiceusers.test()

    test_printServiceRoles = Test_printServiceRoles_script()
    test_printServiceRoless.test()
