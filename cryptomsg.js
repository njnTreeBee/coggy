const EthCrypto = require('eth-crypto');

function createIdentity() {
  // Generate a new key pair
  const identity = EthCrypto.createIdentity();
  
  return {
    address: identity.address,
    privateKey: identity.privateKey
  };
}

function encryptMessage(recipientPublicKey, message, senderPrivateKey) {
  const encryptedMessage = EthCrypto.encryptWithPublicKey(recipientPublicKey, message);

  const payload = {
    message: encryptedMessage,
    sender: EthCrypto.publicKey.toAddress(senderPrivateKey),
  };

  const signature = EthCrypto.sign(senderPrivateKey, EthCrypto.hash.keccak256(payload));

  return {
    message: encryptedMessage,
    signature: signature
  };
}

function decryptMessage(recipientPrivateKey, encryptedMessage, signature, senderPublicKey) {
  const decryptedMessage = EthCrypto.decryptWithPrivateKey(recipientPrivateKey, encryptedMessage);

  const recoveredAddress = EthCrypto.recover(signature, EthCrypto.hash.keccak256({ message: encryptedMessage, sender: senderPublicKey }));
  
  if (recoveredAddress !== senderPublicKey) {
    throw new Error('Invalid sender!');
  }

  return decryptedMessage;
}

module.exports = { createIdentity, encryptMessage, decryptMessage };