// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

//start crowndfunding
//have to give details
//way to collect money
//list to add all startups
// getmoney

contract crowdfunding {
    struct startup {
        string name;
        uint256 goal;
        address startaddress;
        uint256 reached_goal;
        uint256 deadline;
    }
    uint8 number;
    mapping(address => uint256) address_startup;
    mapping(address => bool) boolvalue;
    startup[] public listofstartups;
    uint256 favorite_number;

    function empty() public returns (uint256) {
        return favorite_number;
    }

    function non_empty(uint256 _favoritenumber) public returns (uint256) {
        favorite_number = _favoritenumber;
        return favorite_number;
    }

    function setstruct(
        string memory _name,
        uint256 _goal,
        address _startaddress,
        uint256 _deadline
    ) public {
        require(boolvalue[_startaddress] == false);
        listofstartups.push(
            startup(_name, _goal, _startaddress, 0, block.timestamp + _deadline)
        );
        address_startup[_startaddress] = number;
        boolvalue[_startaddress] = true;
        number += 1;
    }

    function payment(address payable _address)
        public
        payable
        returns (uint256)
    {
        startup storage _startup = listofstartups[address_startup[_address]];
        require(block.timestamp < _startup.deadline);
        if (msg.value + _startup.reached_goal <= _startup.goal) {
            (bool sent, ) = _address.call.value(msg.value)(" ");
            _startup.reached_goal += msg.value;
            require(sent, "Failed to send Ether");
        } else {
            revert();
        }
    }
}
