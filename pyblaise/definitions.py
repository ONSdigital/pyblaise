operations = {
    "get-all-users": {
        "template": "get-all-users.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2018/12/ISecurityManagementService/GetAllUsers201812",
        },
    },
    "request-token": {
        "template": "request-token.xml.template",
        "path": "/Blaise/Security/Services/SecurityTokenService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2016/06/ISecurityTokenService/RequestToken",
        },
    },
    "is-interactive-connection-allowed": {
        "template": "is-interactive-connection-allowed.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "headers": {
            "SOAPAction": "http://www.blaise.com/deploy/2013/03/IDeployService/IsInteractiveConnectionAllowed",
        },
    },
    "get-list-of-instruments": {
        "template": "get-list-of-instruments.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "headers": {
            "SOAPAction": "http://www.blaise.com/deploy/2013/03/IDeployService/GetListOfInstruments",
        },
    },
    "get-roles": {
        "template": "get-roles.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2016/06/ISecurityManagementService/GetRoles",
        },
    },
    "get-all-server-park-definitions": {
        "template": "get-all-server-park-definitions.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "headers": {
            "SOAPAction": "http://www.blaise.com/deploy/2019/06/IDeployService/GetAllServerParkDefinitions201906",
        },
    },
    "get-server-version": {
        "template": "get-server-version.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "headers": {
            "SOAPAction": "http://www.blaise.com/deploy/2019/06/IDeployService/GetServerVersion",
        },
    },
    "get-skills": {
        "template": "get-skills.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2018/12/ISecurityManagementService/GetSkills",
        },
    },
    "get-version": {
        "template": "get-version-response.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "headers": {
            "SOAPAction": "http://www.blaise.com/deploy/2014/09/IDeployService/GetVersionResponse",
        },
    },
    "remove-instrument": {
        "template": "remove-instrument.xml.template",
        "path": "/Blaise/Administer/Services/Deploy",
        "header": {
            "SOAPAction": "http://www.blaise.com/deploy/2013/03/IDeployService/RemoveInstrument",
        },
    },
    "report-user-logout": {
        "template": "report-user-logout.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2016/06/ISecurityManagementService/ReportUserLogout"
        },
    },
    "create-role": {
        "template": "create-role.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2016/06/ISecurityManagementService/CreateRole"
        },
    },
    "change-user-password": {
        "template": "change-user-password.xml.template",
        "path": "/Blaise/Security/Services/SecurityManagementService",
        "headers": {
            "SOAPAction": "http://www.blaise.com/security/2013/03/ISecurityManagementService/ChangePassword"
        },
    },
}

default_headers = {
    "Expect": "100-continue",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "text/xml; charset=utf-8",
}
