pragma solidity ^0.8.0;

import "openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";
import "openzeppelin-solidity/contracts/utils/Counters.sol";

contract AIRegistry is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    struct AICapability {
        uint256 tokenId;
        string capability;
        string description;
        uint iitMeasure;
        bool gwtImplemented;
        bool hasEmbodiedCognition;
        uint complexity;
    }

    mapping(uint256 => AICapability) public aiCapabilities;

    constructor() ERC721("AIRegistry", "AIR") {}

    function registerAI(string memory capability, string memory description, uint iitMeasure, bool gwtImplemented, bool hasEmbodiedCognition, uint complexity) public {
        _tokenIdCounter.increment();
        uint256 newTokenId = _tokenIdCounter.current();
        _safeMint(msg.sender, newTokenId);

        AICapability memory newAICapability = AICapability(newTokenId, capability, description, iitMeasure, gwtImplemented, hasEmbodiedCognition, complexity);
        aiCapabilities[newTokenId] = newAICapability;
    }
}
