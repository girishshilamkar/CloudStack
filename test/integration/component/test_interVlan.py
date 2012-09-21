# -*- encoding: utf-8 -*-
# Copyright 2012 Citrix Systems, Inc. Licensed under the
# Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License.  Citrix Systems, Inc.
# reserves all rights not expressly granted by the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Automatically generated by addcopyright.py at 04/03/2012

""" Component tests for inter VLAN functionality
"""
#Import Local Modules
import marvin
from nose.plugins.attrib import attr
from marvin.cloudstackTestCase import *
from marvin.cloudstackAPI import *
from integration.lib.utils import *
from integration.lib.base import *
from integration.lib.common import *
from marvin.remoteSSHClient import remoteSSHClient
import datetime


class Services:
    """Test inter VLAN services
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
                                    "memory": 64,
                                    },
                         "vpc_offering": {
                                    "name": 'VPC off',
                                    "displaytext": 'VPC off',
                                    "supportedservices": 'Dhcp,Dns,SourceNat,PortForwarding,Vpn,Firewall,Lb,UserData,StaticNat',
                                    },
                         "network": {
                                  "name": "Test Network",
                                  "displaytext": "Test Network",
                                  "vlan": 2370,
                                },
                         "lbrule": {
                                    "name": "SSH",
                                    "alg": "leastconn",
                                    # Algorithm used for load balancing
                                    "privateport": 22,
                                    "publicport": 2222,
                                    "openfirewall": False,
                                },
                         "natrule": {
                                    "privateport": 22,
                                    "publicport": 22,
                                    "protocol": "TCP"
                                },
                         "fw_rule": {
                                    "startport": 1,
                                    "endport": 6000,
                                    "cidr": '55.55.0.0/11',
                                    # Any network (For creating FW rule)
                                },
                         "virtual_machine": {
                                    "displayname": "Test VM",
                                    "username": "root",
                                    "password": "password",
                                    "ssh_port": 22,
                                    "hypervisor": 'XenServer',
                                    # Hypervisor type should be same as
                                    # hypervisor type of cluster
                                    "privateport": 22,
                                    "publicport": 22,
                                    "protocol": 'TCP',
                                },
                         "ostypeid": 'a37063c-258c-4502-a111-d1ff71e116ec',
                         # Cent OS 5.3 (64 bit)
                         "sleep": 60,
                         "timeout": 10,
                         "mode": 'advanced'
                    }


class TestVPCOffering(cloudstackTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_client = super(
                               TestVPCOffering,
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

    @attr(tags=["advanced", "intervlan"])
    def test_01_create_vpc_offering(self):
        """ Test create VPC offering
        """

        # Steps for validation
        # 1. Create VPC Offering by specifying all supported Services
        # 2. VPC offering should be created successfully.

        self.debug("Creating inter VPC offering")
        vpc_off = VpcOffering.create(
                                     self.apiclient,
                                     self.services["vpc_offering"]
                                     )

        self.debug(vpc_off.__dict__)
        self.cleanup.append(vpc_off)

        self.debug("Check if the VPC offering is created successfully?")
        vpc_offs = VpcOffering.list(
                                    self.apiclient,
                                    id=vpc_off.id
                                    )
        self.assertEqual(
                         isinstance(vpc_offs, list),
                         True,
                         "List VPC offerings should return a valid list"
                         )
        return