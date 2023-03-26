pragma solidity ^0.5.17;
pragma experimental ABIEncoderV2;

import "./DenovelScore.sol";

contract DeNovelGovern {
    using SafeMathV2 for uint256;
    // address[] public members;
    address public owner;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 endTime;
        bool executed;
        uint256 yesVotes;
        uint256 noVotes;
        uint256 requireScores;
    }

    mapping(uint256 => mapping(address => bool)) public hasVoted;
    DeNovelScore public credit;
    uint256 public proposalCount;
    uint256 public memberCount;
    uint256 public proposalDuration;
    mapping(uint256 => Proposal) public proposals;
    mapping(address => bool) public memberShip;

    event ProposalCreated(
        uint256 indexed id,
        address indexed proposer,
        uint256 requireScores,
        string description
    );
    event Voted(uint256 indexed id, address indexed voter, bool vote);
    event ProposalExecuted(uint256 indexed id);

    constructor(address creditaddress, uint256 duration) public {
        credit = DeNovelScore(creditaddress);
        proposalDuration = duration;
        owner = msg.sender;
    }

    function getMemberCount() public returns (uint256) {
        return memberCount;
    }

    function getAlliance() public returns (uint256) {
        return credit.allowance(address(this), msg.sender);
    }

    function addMember(address member) public returns (bool) {
        require(msg.sender == owner, "Only owner can add member");
        require(!memberShip[member], "Already been an member");
        memberShip[member] = true;
        credit.transferFrom(msg.sender, member, 10);
        ++memberCount;
        return true;
    }

    function removeMember(address member) public returns (bool) {
        require(msg.sender == owner, "Only owner can remove member");
        require(memberShip[member], "Not an member");
        memberShip[member] = false;
        --memberCount;
        return true;
    }

    function createProposal(string memory description, uint256 requireScores)
        public
        returns (uint256)
    {
        uint256 scores = credit.balanceOf(msg.sender);
        require(scores >= 100, "only members with score >= 100 can proposal");

        uint256 id = ++proposalCount;
        Proposal storage proposal = proposals[id];
        proposal.id = id;
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.endTime = block.timestamp + proposalDuration;
        proposal.requireScores = requireScores;

        // credit.transfer(owner, 100);
        // credit.approve(address(this), 100);
        credit.transferFrom(msg.sender, owner, 100);

        emit ProposalCreated(id, msg.sender, requireScores, description);
        return id;
    }

    function vote(uint256 id, bool vote) public {
        Proposal storage proposal = proposals[id];
        require(
            proposal.endTime > block.timestamp,
            "Proposal voting period has ended"
        );
        require(!hasVoted[id][msg.sender], "Voter has already voted");
        require(memberShip[msg.sender], "Not an member of this DAO");

        uint256 userCredits = credit.balanceOf(msg.sender);
        require(userCredits > 0, "Voter has no credits");

        if (vote) {
            proposal.yesVotes = proposal.yesVotes.add(userCredits);
        } else {
            proposal.noVotes = proposal.noVotes.add(userCredits);
        }
        hasVoted[id][msg.sender] = true;

        emit Voted(id, msg.sender, vote);
    }

    function executeProposal(uint256 id) public {
        Proposal storage proposal = proposals[id];
        require(msg.sender == owner, "Only owner can execute proposal");
        require(
            block.timestamp > proposal.endTime,
            "Proposal voting period has not ended"
        );
        require(!proposal.executed, "Proposal has already been executed");
        require(
            proposal.yesVotes > proposal.noVotes,
            "Proposal has not passed"
        );

        // Add custom logic for proposal execution here
        // ...
        // credit.approve(address(this), 100 + proposal.requireScores);
        credit.transferFrom(
            msg.sender,
            proposal.proposer,
            100 + proposal.requireScores
        );
        // credit.transfer(proposal.proposer, 100 + proposal.requireScores);
        proposal.executed = true;
        emit ProposalExecuted(id);
    }

    function refuseProposal(uint256 id) public {
        Proposal storage proposal = proposals[id];
        require(msg.sender == owner, "Only owner can refuse proposal");
        require(
            block.timestamp > proposal.endTime,
            "Proposal voting period has not ended"
        );
        require(!proposal.executed, "Proposal has already been executed");
        require(
            proposal.yesVotes <= proposal.noVotes,
            "Proposal has not passed"
        );

        // Add custom logic for proposal execution here
        // ...

        proposal.executed = true;
        emit ProposalExecuted(id);
    }

    function getActiveProposals()
        public
        view
        returns (
            uint256[] memory,
            address[] memory,
            string[] memory,
            uint256[] memory,
            uint256[] memory
        )
    {
        uint256 activeProposalCount = 0;

        for (uint256 i = 1; i <= proposalCount; i++) {
            if (
                block.timestamp < proposals[i].endTime && !proposals[i].executed
            ) {
                activeProposalCount++;
            }
        }

        uint256[] memory activeProposalIds = new uint256[](activeProposalCount);
        address[] memory activeProposers = new address[](activeProposalCount);
        string[] memory activeDescriptions = new string[](activeProposalCount);
        uint256[] memory activeEndTimes = new uint256[](activeProposalCount);
        uint256[] memory activeRequireScores = new uint256[](
            activeProposalCount
        );

        uint256 index = 0;
        for (uint256 i = 1; i <= proposalCount; i++) {
            if (
                block.timestamp < proposals[i].endTime && !proposals[i].executed
            ) {
                activeProposalIds[index] = proposals[i].id;
                activeProposers[index] = proposals[i].proposer;
                activeDescriptions[index] = proposals[i].description;
                activeEndTimes[index] = proposals[i].endTime;
                activeRequireScores[index] = proposals[i].requireScores;
                index++;
            }
        }

        return (
            activeProposalIds,
            activeProposers,
            activeDescriptions,
            activeEndTimes,
            activeRequireScores
        );
    }

    function getRecentProposals(uint256 n, uint256 m)
        public
        view
        returns (
            uint256[] memory,
            address[] memory,
            string[] memory,
            uint256[] memory,
            bool[] memory,
            uint256[] memory
        )
    {
        uint256 start = n;
        uint256 end = n + m;

        if (end > proposalCount) {
            end = proposalCount;
        }

        uint256[] memory recentProposalIds = new uint256[](end - start + 1);
        address[] memory recentProposers = new address[](end - start + 1);
        string[] memory recentDescriptions = new string[](end - start + 1);
        uint256[] memory recentEndTimes = new uint256[](end - start + 1);
        bool[] memory recentExecuted = new bool[](end - start + 1);
        uint256[] memory activeRequireScores = new uint256[](end - start + 1);

        uint256 index = 0;
        for (uint256 i = start; i <= end; i++) {
            recentProposalIds[index] = proposals[i].id;
            recentProposers[index] = proposals[i].proposer;
            recentDescriptions[index] = proposals[i].description;
            recentEndTimes[index] = proposals[i].endTime;
            recentExecuted[index] = proposals[i].executed;
            activeRequireScores[index] = proposals[i].requireScores;
            index++;
        }

        return (
            recentProposalIds,
            recentProposers,
            recentDescriptions,
            recentEndTimes,
            recentExecuted,
            activeRequireScores
        );
    }
}
