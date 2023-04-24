const { web3 } = require('./web3');
const { ipfs } = require('./ipfs');
const AIRegistry = require('./build/contracts/AIRegistry.json');
const { PythonShell } = require('python-shell');

const runPythonScript = async () => {
  return new Promise((resolve, reject) => {
    PythonShell.run('extract_capabilities.py', null, (err, results) => {
      if (err) {
        reject(err);
      } else {
        resolve(JSON.parse(results[0]));
      }
    });
  });
};

const registerAI = async (account, ip, nlpData) => {
  // Extract capabilities
  const capabilities = await runPythonScript();

  const aiMetadata = {
    ip: ip,
    nlpData: nlpData,
    capabilities: capabilities
  };

  // Store metadata on IPFS and get the hash
  const ipfsHash = await ipfs.add(JSON.stringify(aiMetadata));

  // Deploy the AIRegistry smart contract
  const networkId = await web3.eth.net.getId();
  const deployedAddress = AIRegistry.networks[networkId].address;
  const abi = AIRegistry.abi;
  const registry = new web3.eth.Contract(abi, deployedAddress);

  // Call the registerAI() function of the smart contract
  const gas = await registry.methods.registerAI(ipfsHash.path).estimateGas({ from: account });
  const result = await registry.methods.registerAI(ipfsHash.path).send({ from: account, gas: gas });

  console.log(`AI registered with IPFS hash: ${ipfsHash.path}`);
};

const main = async () => {
  const account = (await web3.eth.getAccounts())[0];
  const ip = "192.168.0.1";
  const nlpData = "Sample NLP data";
  await registerAI(account, ip, nlpData);
};

main();

