import sys
import contextlib
import uuid


from orchestrator.commands.createNewService import main as CreateNewService
from orchestrator.commands.createNewSubService import main as CreateNewSubService
from orchestrator.commands.createNewServiceRole import main as CreateNewServiceRole
from orchestrator.commands.createNewServiceUser import main as CreateNewServiceUser


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
                "electricidad_%s" % self.suffix ]

        with redirect_argv(args):
            CreateNewSubService()




if __name__ == '__main__':
    test_NewService = Test_NewService_script()
    test_NewService.test()

    test_NewSubService = Test_NewSubService_script()
    test_NewSubService.test()
