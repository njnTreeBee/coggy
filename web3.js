const Web3 = require('web3');

// Connect to the Ethereum network (e.g., local development network, mainnet, or testnet)
const provider = 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID';
const web3 = new Web3(new Web3.providers.HttpProvider(provider));

module.exports = { web3 };
