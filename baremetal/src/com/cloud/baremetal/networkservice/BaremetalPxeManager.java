// Copyright 2012 Citrix Systems, Inc. Licensed under the
// Apache License, Version 2.0 (the "License"); you may not use this
// file except in compliance with the License.  Citrix Systems, Inc.
// reserves all rights not expressly granted by the License.
// You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Automatically generated by addcopyright.py at 04/03/2012
package com.cloud.baremetal.networkservice;

import java.util.List;

import com.cloud.baremetal.database.BaremetalPxeVO;
import com.cloud.deploy.DeployDestination;
import com.cloud.host.HostVO;
import com.cloud.network.Network;
import com.cloud.network.Network.Provider;
import com.cloud.uservm.UserVm;
import com.cloud.utils.component.Manager;
import com.cloud.utils.component.PluggableService;
import com.cloud.vm.NicProfile;
import com.cloud.vm.ReservationContext;
import com.cloud.vm.UserVmVO;
import com.cloud.vm.VirtualMachineProfile;

public interface BaremetalPxeManager extends Manager, PluggableService {
    public enum BaremetalPxeType {
        PING,
    }
    
	boolean prepare(VirtualMachineProfile profile, NicProfile nic, DeployDestination dest, ReservationContext context);

	boolean prepareCreateTemplate(Long pxeServerId, UserVm vm, String templateUrl);
	
	BaremetalPxeType getPxeServerType(HostVO host);
	
	BaremetalPxeVO addPxeServer(AddBaremetalPxeCmd cmd);
	
	BaremetalPxeResponse getApiResponse(BaremetalPxeVO vo);
	
	List<BaremetalPxeResponse> listPxeServers(ListBaremetalPxePingServersCmd cmd);
	
	boolean addUserData(NicProfile nic, VirtualMachineProfile<UserVm> vm);
		
	public static final Network.Service BAREMETAL_PXE_SERVICE = new Network.Service("BaremetalPxeService");
	public static final String BAREMETAL_PXE_CAPABILITY = "BaremetalPxe";
	public static final String BAREMETAL_PXE_SERVICE_PROPERTIES = "baremetalpxe_commands.properties";
	public static final Provider BAREMETAL_PXE_SERVICE_PROVIDER = new Provider("BaremetalPxeProvider", true);;
	public static final Provider BAREMETAL_USERDATA_PROVIDER = new Provider("BaremetaUserdataProvider", true);
}
