import ipaddress
from string import Template

class IP:
    def __init__(self, address, status):
        self.address = address # String: x.x.x.x
        self.status = status # String: 'free' / 'reserved'

    def get_ip_info(anip):
        return 'Network Address: ' + anip.address + ' Status: ' + anip.status

    def reserve_ip(self):
        self.status = 'reserved'
        return 'IP ' + self.address + ' reserved successfully.'

    
    def free_ip(self):
        self.status = 'free'
        return 'IP ' + self.address + ' reserved successfully.'


class Subnet:
    # Type: IP(address, status)
    occupied_ips = []
    # List carries instances created of Subnet obj
    subnets = []

    _intVlanIds = range(4095)
    VlanIds = [str(i) for i in _intVlanIds]
    # 0 is reserved, the rest are free
    VlanIds_statuses = ["reserved"] + ["free"] * 4094
    zip_iterator = zip(VlanIds, VlanIds_statuses)
    VlanIds_dict = dict(zip_iterator)
    
    
    def __init__(self, address, mask, vLanId, name):
        self.address = address
        self.mask = mask
        self.vLanId = vLanId
        self.name = name
        self.__class__.subnets.append(self)
        self.ip_range = [IP(str(ip), 'free') for ip in ipaddress.IPv4Network(self.address+'/'+self.mask)]
        Subnet.update_occupied_ips(self, self.ip_range)

    # Print all subnets
    def view_subnets():
        template = Template('Subnet: $name \n IP: $ipadd \n Mask: $mask \n VlanId: $vlan \n Utilization: $utilization')
        for s in Subnet.subnets: 
            print("--------------------------------")
            print(template.substitute(name = s.name, ipadd = s.address, mask = s.mask, vlan = s.vLanId, utilization = s.utilization))
            print("--------------------------------")


    # Create new subnet     -   Validation: full range of subnet doesn't exist under already identified subnet
    def create_subnet(address, mask, vLanId, name):
        try:
            ip_range = [IP(str(ip), 'free') for ip in ipaddress.IPv4Network(address+'/'+mask)]
        except ValueError:
            return 'Error. Enter a valid address and mask.'
         
        for i_p in ip_range:
            if i_p.address in [x.address for x in Subnet.occupied_ips]:
                return 'Subnet not valid! re-enter a new address and mask and make sure ips are not assigned to another subnet.'
        fresh_subnet = Subnet(address, mask, vLanId, name)
        return 'Subnet ' + fresh_subnet.name + ' was created successfuly.'


    # In: List of IPs   -   Action: Update occupied ips list with occupied ips
    def update_occupied_ips(self, list_of_ips):
        for an_ip in list_of_ips:
            if an_ip.address not in [x.address for x in self.__class__.occupied_ips]:
                self.__class__.occupied_ips.append(an_ip)
        return None


    # In: subnet name   -   Out: subnet object      - Call before get_subnet_object_info to pass the object 
    def get_subnet_object(subnet_name):
        for subnet in Subnet.subnets:
            if subnet_name == subnet.name:
                return subnet
        return None


     # IN: subnet object     -   Action: Print subnet information
    def get_subnet(subnet_name):
        if not subnet_name in [x.name for x in Subnet.subnets]:
            return 'Subnet ' + subnet_name + ' is not recognized'
        template = Template('Subnet: $name \n IP: $ipadd \n Mask: $mask \n VlanId: $vlan \n Utilization: $utilization \n Occupied Ips: $occupied_ips')
        s = Subnet.get_subnet_object(subnet_name)
        list_of_occ_ips = [x.address for x in s.ip_range]
        print("--------------------------------")
        print(template.substitute(name = s.name, ipadd = s.address, mask = s.mask, vlan = s.vLanId, utilization = s.utilization, occupied_ips = list_of_occ_ips ))
        print("--------------------------------")


    # In: Subnet        -       Action: remove the subnet
    def remove_subnet(removed_subnet):
        # using remove() failed me once too many times.
        if removed_subnet.name not in [sn.name for sn in Subnet.subnets]:
            return 'Subnet ' + removed_subnet.name + ' does not exist.'

        subnets_excluding_deleted = []
        for aSubnet in Subnet.subnets:
            if removed_subnet.name == aSubnet.name:
                continue
            subnets_excluding_deleted.append(aSubnet)
        
        Subnet.subnets = subnets_excluding_deleted
        
        occupied_ips_excluding_deleted = []
        for ocip in Subnet.occupied_ips:
            if ocip.address in [x.address for x in removed_subnet.ip_range]:
                continue
            occupied_ips_excluding_deleted.append(ocip)
        
        Subnet.occupied_ips = occupied_ips_excluding_deleted
        return 'Subnet ' + removed_subnet.name + 'was removed successfully.'
 

    # In: Subnet    -   Action: Assign VLan Id to subnet
    def assign_VlanId(subnet, VlanId):
        # Invalid vlan id
        if not VlanId in Subnet.VlanIds_dict:
            return VlanId + ' is invalid. retry with a valid Vlan id.'
            
        # Invalid subnet name
        if not subnet.name in [s.name for s in Subnet.subnets]:
           return subnet.name + ' is not recognized as a subnet. use ::view_subnets to check for valid names.'

        # Already assigned
        if subnet.vLanId == VlanId:
            return 'vlanId '+VlanId+' is already assigned. retry with different vlan Id.'

        # Reserved to another subnet vlan id
        if Subnet.VlanIds_dict[VlanId] == 'reserved':
            return 'VlanId ' + str(VlanId) + ' is reserved. ' + 'free VlanId suggestion: ' +  Subnet.get_free_VlanId()
        
        # Free old assigned vLan id
        if subnet.vLanId != None:
            Subnet.VlanIds_dict[subnet.vLanId] = 'free'
        
        # Assign new Vlan id
        subnet.vLanId = VlanId
        # Reserve the newly assigned vlan id
        Subnet.VlanIds_dict[VlanId] = 'reserved'
        return 'VlanId ' + str(VlanId) + ' is assigned to subnet: ' + subnet.name


    # In: Subnet    -   Action: Remove current VLan Id of subnet
    def remove_VlanId(subnet):
        Subnet.VlanIds_dict[subnet.vLanId] = 'free'
        subnet.vLanId = None
        return 'successfully remove subnet ' + subnet.name + ' vlanId'


    # In: IP Address    -   Out: Parent subnet
    def get_parent_subnet(an_IPAddress):
        for subnet in Subnet.subnets:
            if an_IPAddress in [x.address for x in subnet.ip_range]:
                return subnet.name

        return 'ip: ' + an_IPAddress + ' does not belong in any subnet.'


    # In: Ip Address    -   Out: IP object
    def get_ip(address):
        for ipp in Subnet.occupied_ips:
            if address == ipp.address:
                return ipp
        return None


    def reserve_ip(input_ip):
        if input_ip == '':
            for random_ip in [x for x in Subnet.occupied_ips]:
                if random_ip.status == 'free':
                    random_ip.reserve_ip()
                    return random_ip.address + ' is reserved successully!'
            return 'No free ips. Use add_subent to add ips.'

        input_ipObj = Subnet.get_ip(input_ip)
        # IP is not recognized
        if input_ipObj == None:
            return input_ip + ' is not recognized. Use view_ips to view valid ips.'
        
        # IP is reserved 
        if input_ipObj.status == 'reserved':
            return input_ip + ' is reserved. Use view_ip to check an IP availablity' 
        
        # Success
        input_ipObj.reserve_ip()
        return input_ipObj.address + 'reserved successully!'


    def reserve_ip_use_subnet(input_subnet):
        input_subnetObj = Subnet.get_subnet_object(input_subnet)
        # IP is not recognized
        if input_subnetObj == None:
            return input_subnet + ' subnet name is not recognized. Use view_ips to view valid ips.'
        
        for i_p in input_subnetObj.ip_range:
            if i_p.status == 'free':
                print('reserving: ', i_p.address)
                i_p.reserve_ip()
                return i_p.address + ' reserved successfully.' 
        return 'subnet ' + input_subnet + ' has no free ips.'
    

    def free_ip(input_ip):
        input_ipObj = Subnet.get_ip(input_ip)
        # IP is not recognized
        if input_ipObj == None:
            return input_ip + ' is not recognized. Use view_ips to view valid ips.'
        
        # IP is free 
        if input_ipObj.status == 'f':
            return input_ip + 'is already free.'
        
        # Success
        input_ipObj.free_ip()
        return input_ipObj.address + ' is freed successully!'


    # Used to suggest free Vlan Id
    @staticmethod
    def get_free_VlanId():
        for i in range(4095):
            if Subnet.VlanIds_dict[i] == 'free':
                return str(i)
        return 'No Vlan Id avaliable'

    # Used to print subnet info
    @property
    def utilization(self):
        total_ips = len(self.ip_range) 
        utilized_ips = 0
        for ip in self.ip_range:
            if ip.status == 'free':
                continue
            utilized_ips += 1
        return utilized_ips / total_ips * 100


guide = '''use a command to perform action...
available commands:
- help
- add_subnet    -subnet_name -subnet_address -subnet_mask -optional_*subnet_vlanId
- remove_subnet     -subnet_name                
- view_subnets                                    ::get all configured subnets info
- view_ips                                        ::get all valid IPs in the network  
- get_subnet        -subnet_name                  ::get full subnet info
- get_ip -ip                                      ::get IP info
- sub_reserve_ip    -subnet_name
- reserve_ip        -optional_*ip                   
- free_ip           -ip 
- assign_vlanid     -subnet -vlanId               ::assign VLan Id to subnet  ::  overrides existing value
- remove_vlanid     -subnet_name                  ::delete VLan Id assigned for subnet
- get_ips                                         ::get IPs reserved by all the subnets in the network
- quit
'''

print('Program ##IPAM## Started.')
print(guide)

while True:
    command = input('Enter a command: ')
    command_captured = False

    if command == 'help':
        print(guide)

    if command == 'view_subnets':
        command_captured = True
        Subnet.view_subnets()
    
    if command == 'quit':
        break
    
    # Todo: check creating subnet with already occupied ip not failing
    if command == 'add_subnet':
        command_captured = True
        print('creating new subnet..')
        aname = input('Name: ')
        address = input('Address: ')
        mask = input('Mask: ')
        vLlanId = input('press ENTER. Or Enter a vLanId: ')
        if vLlanId == '':
            vLlanId = None
        print(Subnet.create_subnet(address, mask, vLlanId, aname))
    
    if command == 'remove_subnet':
        command_captured = True
        subnet_name = input('Enter subnet name for removal: ')
        subnet_to_remove = Subnet.get_subnet_object(subnet_name)
        print(Subnet.remove_subnet(subnet_to_remove))
    
    if command == 'view_ips':
        command_captured = True
        print([x.address for x in Subnet.occupied_ips])
    
    if command == 'remove_vlanid':
        command_captured = True
        subnet_name = input('Enter subnet name for vlanId reset:')
        subnetObj = Subnet.get_subnet_object(subnet_name)
        print(Subnet.remove_VlanId(subnetObj))

    if command == 'assign_vlanid':
        command_captured = True
        subnet_name = input('Enter subnet name:')
        subnetObj = Subnet.get_subnet_object(subnet_name)
        if subnetObj == None:
            print(subnet_name + ' is not recognized as a subnet_name. Use view_subnets to view valid subnet names.')
            continue
        vlanId = input('Enter vlan id to assign to ' + subnet_name + ':')

        print(Subnet.assign_VlanId(subnetObj, vlanId))

    if command == 'get_ip':
        command_captured = True
        input_ip = input('Enter IP Address: ')
        ipObj = Subnet.get_ip(input_ip)
        if ipObj == None:
            print('ip address ' + input_ip + ' is not recognized. Use get_ips command to view the valid ip addresses.')
            continue
        print('---------------------')
        print(IP.get_ip_info(ipObj))
        print('Parent subnet: ', Subnet.get_parent_subnet(input_ip))
        print('---------------------')
        
    if command == 'reserve_ip':
        command_captured = True
        ip_requested = input('Press enter to reserve any free ip. Or Enter an IP address to reserve: ')
        print(Subnet.reserve_ip(ip_requested))

    if command == 'free_ip': 
        command_captured = True
        ip_requested = input('Enter an IP address to free: ')
        print(Subnet.free_ip(ip_requested))

    if command == 'sub_reserve_ip':
        command_captured = True
        subnet_name = input('Enter subnet name: ')
        print(Subnet.reserve_ip_use_subnet(subnet_name))

    if command == 'get_subnet':
        command_captured = True
        input_subnet_name = input('Enter subnet name:')
        Subnet.get_subnet(input_subnet_name)

    if not command_captured:
        print(command+' is not a valid command')
    

  
print('Program ##IPAM## Finished.')


