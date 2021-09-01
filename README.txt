Command Line Tool  IP Management System.


Usage: 

When prompted to enter a command, type in one of the following commands:
- help
- add_subnet        -subnet_name -subnet_address -subnet_mask -optional_*subnet_vlanId
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


add_subnet:
  - Validations:
     - Valid Address/Mask.
     - IP Range is not occupied by another subnet.
  - Details
     - Update list of occupied ips by the network
 
     
remove_subnet:
  - Validations:
     - Subnet name is already configured.
  - Details:
     - Remove subnet ip range from list of occupied ips by the network.
     - Remove subnet from configured subnets.
     
     
view_subnets:
  - Action:
    - Print all configured subnets.
   - Info: Address, Mask, VlanId, Utilization %


view_ips:
  - Action
    - Print all occupied Ip addresses by the network.
    
    
get_subnet:
    - Action:
      - Print all configured subnets.
    - Info: Address, Mask, VlanId, Utilization %, IP Range.
    

get_ip: -IPAddress
    - Action:
      Get specific IP info: Parent subnet, Address, Status(free/reserved)
  


sub_reserve_ip: -subnet_name
     - Action:
      Reserve a free IP address in a subnet 
      
   
reserve_ip: *ip
     - Action:
     If ip is provided reserve ip. If not reserve any free ip.
     
     
free_ip: -ip
      - Action
      Change ip status to free.
      
      
      
assign_vlanid: -subnet -vlanId 
      - Action
      Assing vlanId to subnet.


remove_vlanid: -subnet
      - Action
      Delete vlanId of subnet
      
      
get_ips:
      - Action
      return all ip addresses occupied by the network
       


 quit:
      - Action
      QUIT


