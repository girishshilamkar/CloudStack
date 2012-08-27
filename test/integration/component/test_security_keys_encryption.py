""" P1 tests for Security Keys Encryption
"""
#Import Local Modules
from nose.plugins.attrib import attr
from integration.lib.base import *
from integration.lib.common import *
from integration.lib.utils import *
from marvin import remoteSSHClient
from marvin.cloudstackAPI import *
from marvin.cloudstackTestCase import *
import datetime
import marvin


class Services:
    """Test Security encryption Services
    """

    def __init__(self):
        self.services = {
                        "account": {
                                    "email": "test@test.com",
                                    "firstname": "Test",
                                    "lastname": "User",
                                    "username": "test",
                                    # Random characters are appended for unique
                                    # username
                                    "password": "password",
                         },
                         "service_offering": {
                                    "name": "Tiny Instance",
                                    "displaytext": "Tiny Instance",
                                    "cpunumber": 1,
                                    "cpuspeed": 100,
                                    # in MHz
                                    "memory": 64,
                                    # In MBs
                        },
                        "virtual_machine": {
                                    "displayname": "TestVM",
                                    "username": "root",
                                    "password": "password",
                                    "ssh_port": 22,
                                    "hypervisor": 'XenServer',
                                    "privateport": 22,
                                    "publicport": 22,
                                    "protocol": 'TCP',
                                },
                        "vpn_user": {
                                   "username": "test",
                                   "password": "test",
                                },
                         "host": {
                                   "username": "root",
                                   "password": "password",
                                },
                         "globalconfig": {
                                   "security.hash.key": "test",
                                    "vmware.guest.vswitch" : "test",
                                    "vmware.public.vswitch" : "test",
                                    "vmware.private.vswitch" : "test",
                                    "kvm.guest.network.device" : "test",
                                    "ovm.guest.network.device" : "test",
                                    "xen.guest.network.device" : "test",
                                    "kvm.public.network.device" : "test",
                                    "ovm.public.network.device" : "test",
                                    "xen.public.network.device" : "test",
                                    "kvm.private.network.device" : "test",
                                    "ovm.private.network.device" : "test",
                                    "xen.private.network.device" : "test",
                                    "xen.storage.network.device1" : "test",
                                    "xen.storage.network.device2" : "test",
                                    "alert.smtp.password" : "test",
                                    "project.smtp.password" : "test",
                                },
                        "ostypeid": 'bc66ada0-99e7-483b-befc-8fb0c2129b70',
                        # Cent OS 5.3 (64 bit)
                        "sleep": 60,
                        "timeout": 10,
                        "mode": 'advanced'
                    }


class TestSecurityKeysEncryption(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_client = super(
                               TestSecurityKeysEncryption,
                               cls
                               ).getClsTestClient().getApiClient()
        cls.services = Services().services
        # Get Zone, Domain and templates
        cls.domain = get_domain(cls.api_client, cls.services)
        cls.zone = get_zone(cls.api_client, cls.services)

        template = get_template(
                            cls.api_client,
                            cls.zone.id,
                            cls.services["ostypeid"]
                            )
        cls.services["virtual_machine"]["zoneid"] = cls.zone.id

        cls.services["template"] = template.id

        # Create Account, VMs etc
        cls.account = Account.create(
                            cls.api_client,
                            cls.services["account"],
                            domainid=cls.domain.id
                            )
        cls.services["account"] = cls.account.account.name

        cls.service_offering = ServiceOffering.create(
                                            cls.api_client,
                                            cls.services["service_offering"]
                                            )
        cls.virtual_machine = VirtualMachine.create(
                                cls.api_client,
                                cls.services["virtual_machine"],
                                templateid=template.id,
                                accountid=cls.account.account.name,
                                domainid=cls.account.account.domainid,
                                serviceofferingid=cls.service_offering.id
                                )

        cls.public_ip = PublicIPAddress.create(
                                           cls.api_client,
                                           cls.virtual_machine.account,
                                           cls.virtual_machine.zoneid,
                                           cls.virtual_machine.domainid,
                                           cls.services["virtual_machine"]
                                           )

        cls._cleanup = [
                        cls.service_offering,
                        cls.account,
                        ]
        return

    @classmethod
    def tearDownClass(cls):
        try:
            #Cleanup resources used
            cleanup_resources(cls.api_client, cls._cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []
        return

    def tearDown(self):
        try:
            #Clean up, terminate the created instance, volumes and snapshots
            cleanup_resources(self.apiclient, self.cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    @attr(tags = ["advanced", "basic"])
    def test_vm_instance_vnc_password(self):
        """ Verify vm_instance table's vnc_password column encryption """


        #Steps,
        #Deploy  a VM
        #Once VM is running goto db Server
        #Validation,
        #Verify vm_instance table's vnc_password column is encrypted

        qresultset = self.dbclient.execute(
                        "select vnc_password from vm_instance where uuid = '%s';" \
                        % self.virtual_machine.id
                        )
        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )
        self.assertNotEqual(
                         qresultset[0][0],
                         self.services["virtual_machine"]["password"],
                         "Check vnc_password in vm_instance table to verify encryption"
                         )
        return

    @attr(tags = ["advanced"])
    def test_vpn_users_password(self):
        """ Verify vpn_users table's password column encryption """


        #Steps,
        #Deploy a VM
        #Aquire a IP
        #Enable VPN on the acquired  IP
        #Add VPN user
        #Validations,
        #Verify vpn_users table's password column is encrypted

        self.debug("Created VPN with public IP: %s" % self.public_ip.ipaddress.id)

        #Assign VPN to Public IP
        vpn = Vpn.create(
                        self.apiclient,
                        self.public_ip.ipaddress.id,
                        account=self.account.account.name,
                        domainid=self.account.account.domainid
                        )

        self.debug("Created VPN user for account: %s" %
                                    self.account.account.name)

        vpnuser = VpnUser.create(
                                 self.apiclient,
                                 self.services["vpn_user"]["username"],
                                 self.services["vpn_user"]["password"],
                                 account=self.account.account.name,
                                 domainid=self.account.account.domainid
                                 )

        qresultset = self.dbclient.execute(
                        "select password from vpn_users where uuid = '%s';" \
                        % vpnuser.id
                        )

        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )

        self.assertNotEqual(
                         qresultset[0][0],
                         self.services["vpn_user"]["password"],
                         "Check password in vpn_users table to verify encryption"
                         )

    @attr(tags = ["advanced", "basic"])
    def test_user_secret_key(self):
        """ Verify user table's SECRET key column encryption """
        #Steps,
        #generate key for the user of the account
        #Validations,
        #Verify user table's secret key column is encrypted


        user_keys = User.registerUserKeys(self.apiclient, self.account.account.user[0].id)
        qresultset = self.dbclient.execute(
                        "select secret_key from user where uuid = '%s';" \
                        % self.account.account.user[0].id
                        )

        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )

        self.assertNotEqual(
                         qresultset[0][0],
                         user_keys.secretkey,
                         "Check secret key in users table to verify encryption"
                         )
        return

    @attr(tags = ["advanced", "basic"])
    def test_host_password(self):
        """ Verify host details table's  value column encryption where name is password """


        #Validations,
        #Verify host details table's value column is encrypted where name is password

        hosts = list_hosts(
                           self.apiclient,
                           zoneid=self.services["virtual_machine"]["zoneid"],
                           type='Routing',
                           state='Up'
                           )
        self.assertEqual(
                        isinstance(hosts, list),
                        True,
                        "Check list host returns a valid list"
                        )

        host = hosts[0]

        qresultset = self.dbclient.execute(
                        "select id from host where uuid = '%s';" \
                        % host.id
                        )

        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )

        hostid = qresultset[0][0]

        qresultset = self.dbclient.execute(
                        "select value from host_details where host_id = '%s' and name='password';" \
                        % hostid
                        )

        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )

        self.assertNotEqual(
                         qresultset[0][0],
                         self.services["host"]["password"],
                         "Check password field value in host_details table to verify encryption"
                         )
        return

    @attr(tags = ["advanced", "basic"])
    def test_configurations_value_encryption(self):
        """ verify configuration tables following name records value field  are encrypted """


        #Steps
        #verify configuration tables following name records value field  are encrypted
        #security.hash.key
        #vmware.guest.vswitch
        #vmware.public.vswitch
        #vmware.private.vswitch
        #kvm.guest.network.device
        #ovm.guest.network.device
        #xen.guest.network.device
        #kvm.public.network.device
        #ovm.public.network.device
        #xen.public.network.device
        #kvm.private.network.device
        #ovm.private.network.device
        #xen.private.network.device
        #xen.storage.network.device1
        #xen.storage.network.device2
        #alert.smtp.password
        #project.smtp.password
        #Validations,
        #Verify configuration  table's following name records value filed is encrypted

        for k, v in self.services["globalconfig"].items():

            #setting some test value to the configuration
            Configurations.update(self.apiclient, k, v)

            #fetching the value of the configuration from DB
            qresultset = self.dbclient.execute(
                        "select value from configuration where name = '%s';" \
                        % k
                        )

            self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )

            config_value = qresultset[0][0]

            #verifying the value from db and set are not equal and the value in db is encrypted
            self.assertNotEqual(
                         config_value,
                         v,
                         "Check configuration value in database is not equal to value set to verify the value is encrypted"
                         )

            #Setting the configuration value back to None as default value
            Configurations.update(self.apiclient, k)
        return


class TestSingleSignOnEncryption(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_client = super(
                               TestSingleSignOnEncryption,
                               cls
                               ).getClsTestClient().getApiClient()
        cls.services = Services().services
        # Get Zone, Domain and templates
        cls.domain = get_domain(cls.api_client, cls.services)
        cls.zone = get_zone(cls.api_client, cls.services)
        cls._cleanup = []
        return

    @classmethod
    def tearDownClass(cls):
        try:
            #Cleanup resources used
            cleanup_resources(cls.api_client, cls._cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    def setUp(self):
        self.apiclient = self.testClient.getApiClient()
        self.dbclient = self.testClient.getDbConnection()
        self.cleanup = []
        return

    def tearDown(self):
        try:
            #Clean up, terminate the created network offerings
            cleanup_resources(self.apiclient, self.cleanup)
        except Exception as e:
            raise Exception("Warning: Exception during cleanup : %s" % e)
        return

    @attr(tags=["advanced", "configuration", "advancedns", "simulator",
                "api", "basic", "eip", "sg"])
    def test_SingleSignOnEncryption(self):
        """List listConfigurations API should get decrypted
            security.singlesignon.key
        """

        # Steps for validation
        # 1. listConfigurations - security.singlesignon.key
        # Validate the following
        # 1. assert that the field is encrypted (value mismatch)
        # 2. assert that section of the DB for this config is "Secure"
        #    and not "Hidden"

        config = Configurations.list(
                                    self.apiclient,
                                    name='security.singlesignon.key',
                                    listall=True
                                    )
        self.assertEqual(
                isinstance(config, list),
                True,
                "List configurations should have security.singlesignon.key"
                )

        config_value = config[0].value
        config_category = config[0].category
        qresultset = self.dbclient.execute(
                        "select value from configuration where name='security.singlesignon.key';"
                        )
        self.assertEqual(
                         isinstance(qresultset, list),
                         True,
                         "Check DB query result set for valid data"
                         )
        self.assertNotEqual(
                         qresultset[0][0],
                         config_value,
                         "The security.singlesignon.key is not encrypted"
                         )
        self.assertEqual(
                         config_category,
                         "Secure",
                         "The configuration category should be secure"
                         )
        return
