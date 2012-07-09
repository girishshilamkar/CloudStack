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
package com.cloud.network.as;

import java.util.Date;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.Table;

import com.cloud.utils.db.GenericDao;
import com.cloud.utils.net.NetUtils;

@Entity
@Table(name="autoscale_policies")
@Inheritance(strategy=InheritanceType.JOINED)
public class AutoScalePolicyVO implements AutoScalePolicy {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    @Column(name="id")
    long id;

    @Column(name="uuid")
    String uuid;

    @Column(name="zone_id")
    protected long zoneId;

    @Column(name="domain_id")
    private long domainId;

    @Column(name="account_id")
    private long accountId;

    @Column(name="duration")
    private Integer duration;

    @Column(name="quiet_time", updatable=true, nullable = false)
    private Integer quietTime = NetUtils.DEFAULT_AUTOSCALE_POLICY_QUIET_TIME;

    @Column(name="action", updatable=false, nullable = false)
    private String action;

    @Column(name=GenericDao.REMOVED_COLUMN)
    protected Date removed;

    @Column(name=GenericDao.CREATED_COLUMN)
    protected Date created;

    public AutoScalePolicyVO() {
    }

    public AutoScalePolicyVO(long zoneId, long domainId, long accountId, Integer duration, Integer quietTime, String action) {
        this.uuid = UUID.randomUUID().toString();
        this.zoneId = zoneId;
        this.domainId=domainId;
        this.accountId = accountId;
        this.duration = duration;
        if (quietTime != null) {
        	this.quietTime = quietTime;
        }
        this.action = action;
    }

    @Override
    public String toString() {
        return new StringBuilder("AutoScalePolicy[").append("id-").append(id).append("]").toString();
    }
    @Override
	public long getId() {
        return id;
    }

    public String getUuid() {
        return uuid;
    }

    @Override
	public long getZoneId() {
        return zoneId;
    }

    @Override
	public long getDomainId() {
        return domainId;
    }

    @Override
	public long getAccountId() {
        return accountId;
    }

    @Override
	public Integer getDuration() {
        return duration;
    }

    @Override
	public Integer getQuietTime() {
        return quietTime;
    }

    @Override
	public String getAction() {
        return action;
    }

    public Date getRemoved() {
        return removed;
    }

    public Date getCreated() {
        return created;
    }

}
