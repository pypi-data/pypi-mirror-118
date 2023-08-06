import re
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from vmanage.api.authentication import Authentication
from vmanage.api.device_templates import DeviceTemplates


def vmanage_argument_spec():
    return dict(host=dict(type='str', required=True, fallback=(env_fallback, ['VMANAGE_HOST'])),
                port=dict(type='str', required=False, fallback=(env_fallback, ['VMANAGE_PORT'])),
                user=dict(type='str', required=True, fallback=(env_fallback, ['VMANAGE_USERNAME'])),
                password=dict(type='str', required=True, fallback=(env_fallback, ['VMANAGE_PASSWORD'])),
                validate_certs=dict(type='bool', required=False, default=False),
                timeout=dict(type='int', default=30)
                )


class Vmanage(object):

    def __init__(self, module, function=None):
        self.module = module
        self.params = module.params
        self.result = dict(changed=False)
        self.params['force_basic_auth'] = True
        self.username = self.params['user']
        self.password = self.params['password']
        self.host = self.params['host']
        self.port = self.params['port']
        self.timeout = self.params['timeout']

        self.__auth = None

    @property
    def auth(self):
        if self.__auth is None:
            self.__auth = Authentication(host=self.host, user=self.username, password=self.password).login()
        return self.__auth

    def exit_json(self, **kwargs):
        # self.logout()
        """Custom written method to exit from module."""

        self.result.update(**kwargs)
        self.module.exit_json(**self.result)

    def fail_json(self, msg, **kwargs):
        # self.logout()
        """Custom written method to return info on failure."""

        self.result.update(**kwargs)
        self.module.fail_json(msg=msg, **self.result)

    def get_template_variables(self, template_id):
        vmanage_device_templates = DeviceTemplates(self.auth, self.host)
        return_dict = {}
        response = vmanage_device_templates.get_template_input(template_id)

        if response:
            if 'columns' in response:
                column_list = response['columns']

                regex = re.compile(r'\((?P<variable>[^(]+)\)')

                for column in column_list:
                    if column['editable']:
                        # match = regex.search(column['title'])
                        match = regex.findall(column['title'])
                        if match:
                            # variable = match.groups('variable')[0]
                            variable = match[-1]
                            return_dict[variable] = column['property']

        return return_dict

    def get_template_optional_variables(self, template_id):
        vmanage_device_templates = DeviceTemplates(self.auth, self.host)
        return_dict = {}
        response = vmanage_device_templates.get_template_input(template_id)

        if response:
            if 'columns' in response:
                column_list = response['columns']

                regex = re.compile(r'\((?P<variable>[^(]+)\)')

                # The following can be removed once the API will mark as optional
                # the nexthop value of a static route that has been marked as optional
                regexYangStaticR = re.compile(r'.*/vpn-instance/ip/route/.*/prefix')
                regex_yang_nexthop = re.compile(r'.*/vpn-instance/ip/route/(?P<staticR>.*)/next-hop/.*/address')
                optionalStaticRoutesList = []
                # Until here

                # The following can be removed once the API will mark as optional
                # all the vrrp attributes once the vrrp grp-id has been marked optional
                regexYangVRRPgrpID = re.compile(r'.*/vrrp/.*/grp-id')
                regexYangVRRPpriority = re.compile(r'.*/vrrp/(?P<VVRPgrp>.*)/priority')
                regexYangVRRPtimer = re.compile(r'.*/vrrp/(?P<VVRPgrp>.*)/timer')
                regexYangVRRPtrackPrefix = re.compile(r'.*/vrrp/(?P<VVRPgrp>.*)/track-prefix-list')
                regexYangVRRPtrackOMP = re.compile(r'.*/vrrp/(?P<VVRPgrp>.*)/track-omp')
                regexYangVRRPipAddress = re.compile(r'.*/vrrp/(?P<VVRPgrp>.*)/ipv4/address')
                optionalVRRPvariales = []
                # Until here

                # The following can be removed once the API will mark as optional
                # all the logging attributes once the logging has been marked optional
                regexYangLoggingServerName = re.compile(r'///logging/server/.*/name')
                regexYangLoggingSourceInt = re.compile(r'///logging/server/(?P<LoggServer>.*)/source-interface')
                regexYangLoggingVPN = re.compile(r'///logging/server/(?P<LoggServer>.*)/vpn')
                regexYangLoggingPriority = re.compile(r'///logging/server/(?P<LoggServer>.*)/priority')
                optionalLoggingVariales = []
                # Until here

                for column in column_list:

                    # The following can be removed once the API will mark as optional
                    # the nexthop value of a static route that has been marked as optional

                    # Based on the regular expression above we match
                    # static routes and next-hop variables based on the YANG variable
                    # a static route looks like this /1/vpn-instance/ip/route/<COMMON_NAME_OF_THE_ROUTE>/prefix
                    # a next-hop looks like this /1/vpn-instance/ip/route/<COMMON_NAME_OF_THE_ROUTE>/next-hop/<COMMON_NAME_OF_THE_NH>/address

                    # If we find a static route and this is optional we
                    # store its common name into an array
                    # we don't add this parameter to the return list now
                    # since it will be added later
                    isStaticR = regexYangStaticR.match(column['property'])
                    if isStaticR and column['optional']:
                        match = regex.findall(column['title'])
                        if match:
                            variable = match[-1]
                            optionalStaticRoutesList.append(variable)

                    # If we find a next-hop we extrapolate the common name
                    # of the static route. If we have already found that
                    # common name and we know it is optional we will add
                    # this next-hop paramter to the return list since it
                    # will be optional as well

                    # ALL OF THIS IS BASED ON THE ASSUMPTION THAT STATIC ROUTES
                    # ARE LISTED BEFORE NEXT-HOP VALUES
                    nextHopStaticR = regex_yang_nexthop.findall(column['property'])
                    if nextHopStaticR:
                        if nextHopStaticR[0] in optionalStaticRoutesList:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']

                    # Until here

                    # The following can be removed once the API will mark as optional
                    # the attributes for vrrp as optional if the whole vrrp has been
                    # marked as optional

                    # Based on the regular expression above we match
                    # vrrp atributes based on the YANG variable

                    # If we find a VRRP grp ID and this is optional we
                    # store its common name into an array
                    # we don't add this parameter to the return list now
                    # since it will be added later
                    isVRRP = regexYangVRRPgrpID.match(column['property'])
                    if isVRRP and column['optional']:
                        match = regex.findall(column['title'])
                        if match:
                            variable = match[-1]
                            optionalVRRPvariales.append(variable)

                    # If we find a any vrrp attribute we extrapolate the common name
                    # If we have already found that
                    # common name and we know it is optional we will add
                    # this paramter to the return list since it
                    # will be optional as well

                    # ALL OF THIS IS BASED ON THE ASSUMPTION THAT VRRP GRP-ID is
                    # LISTED BEFORE ALL THE OTHER ATTRIBUTES
                    VRRPpriority = regexYangVRRPpriority.findall(column['property'])
                    VRRPtimer = regexYangVRRPtimer.findall(column['property'])
                    VRRPtrackPrefix = regexYangVRRPtrackPrefix.findall(column['property'])
                    VRRPipAddress = regexYangVRRPipAddress.findall(column['property'])
                    VRRPtrackOMP = regexYangVRRPtrackOMP.findall(column['property'])
                    if VRRPpriority:
                        if VRRPpriority[0] in optionalVRRPvariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif VRRPtimer:
                        if VRRPtimer[0] in optionalVRRPvariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif VRRPtrackPrefix:
                        if VRRPtrackPrefix[0] in optionalVRRPvariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif VRRPipAddress:
                        if VRRPipAddress[0] in optionalVRRPvariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif VRRPtrackOMP:
                        if VRRPtrackOMP[0] in optionalVRRPvariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                                # Until here

                    # Same logic for logging optional variables
                    isLogging = regexYangLoggingServerName.match(column['property'])
                    if isLogging and column['optional']:
                        match = regex.findall(column['title'])
                        if match:
                            variable = match[-1]
                            optionalLoggingVariales.append(variable)

                    LoggingSourceInt = regexYangLoggingSourceInt.findall(column['property'])
                    LoggingVPN = regexYangLoggingVPN.findall(column['property'])
                    LoggingPriority = regexYangLoggingPriority.findall(column['property'])

                    if LoggingSourceInt:
                        if LoggingSourceInt[0] in optionalLoggingVariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif LoggingVPN:
                        if LoggingVPN[0] in optionalLoggingVariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']
                    elif LoggingPriority:
                        if LoggingPriority[0] in optionalLoggingVariales:
                            match = regex.findall(column['title'])
                            if match:
                                variable = match[-1]
                                return_dict[variable] = column['property']

                    # Until here

                    if column['editable'] and column['optional']:
                        match = regex.findall(column['title'])
                        if match:
                            variable = match[-1]
                            return_dict[variable] = column['property']

        return return_dict
