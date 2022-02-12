pragma solidity ^0.8.0;


contract Patient_Data {
    address private Head; //Have the main rights to alter

    // patient report
    struct Report {
        string name; //patient name
        address patientAddress; //patient address
        string[] symptoms; //array of symptoms
        string prediction; //prediction done by the model
         
    }

    
    //mapping the patient's address to reports
    mapping(address => Report[]) public ledger;


    constructor () {
        Head = msg.sender; // assigning the contract deployer, the Head
    }

    // to check accessibility
    modifier onlyHead() {
        require(msg.sender == Head,
        "Sorry you are not authorised. !!");
        _;
    }

    // to change Head
    function changeHead(address _newHead) onlyHead public {
        Head = _newHead;
    }

    //function to upload the patient report
    function upload (string memory _name, string[] memory _symptoms, string memory _pridiction) public {
        ledger[msg.sender].push(Report({
            name: _name,
            patientAddress: msg.sender,
            symptoms: _symptoms,
            prediction: _pridiction
        }));
    }

    
    //doctor to current patient
    mapping(address => address) DoctorToPatient;

    // patient giving access
    // call by patient
    function giveAccess (address _doctor) public {
        DoctorToPatient[_doctor] = msg.sender;
    }

    // doctor recieving data 
    // call by doctor
    function recieveByDoctor () view public returns (Report[] memory) {
        require(ledger[DoctorToPatient[msg.sender]][0].patientAddress == DoctorToPatient[msg.sender], "Patient has not permitted yet");
        return ledger[DoctorToPatient[msg.sender]];
    }

    //patient recieving data
    // call by patient
    function recieveByPatient () view public returns (Report[] memory) {
        require(ledger[msg.sender][0].patientAddress == msg.sender, "Your dont have any report yet");
        return ledger[msg.sender];
    }

    //break the access
    // call from doctor 
    function breakAccess () public {
        DoctorToPatient[msg.sender] = address(0);
    }

    //break access by patient
    //call from patient
    function breakAccessByPatient (address _doctor) public {
        require(DoctorToPatient[_doctor]==msg.sender, "This is not your Doctor");
        DoctorToPatient[_doctor] = address(0);
    }


}