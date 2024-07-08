# Jito Handler
Helper Project for Controlling Solana Transactions Using the Jito Network


# Setup

Enter the Project Directory
```commandline
PS:> cd jito-handler
```

Install Requirements (Windows/Powershell)
```commandline
PS:> pip install -r requirements.txt
```

Create .env file
```commandline
PS:> New-Item -ItemType File -Path ./.env
```

Set Environment Variables
```commandline
SOLANA_PUBLIC_KEY=[YOUR_PUBLIC_KEY]
MAIN_WALLET=[MAIN_WALLET_ADDRESS]  // Testing Purposes
TEST_WALLET=[TEST_WALLET_ADDRESS]  // Testing Purposes
SEED_PHRASE=[YOUR_SOLANA_SEED_PRHASE]   // Testing Purposes
```

### Seed Phrases

Using the Solana CLI, you **_should_** be able to use the solana-keygen function to confirm your solana public key matches the keypair derived from your seed phrase.

**Unfortunately** it does not... (for me anyway) in my case my Wallet _[123xEfGu... etc]_ with the seed phrase _[random, words, etc]_  and password of _[supersecretpassword123]_ generates an entirely different wallet address.

What this means is that I cannot accurately simulate a transaction on the testnet because of "pubkey-keypair mismatch".

I believe this happens due to certain wallets (SolFlare, Phantom Wallet, etc) creating subwallets with derivation paths hidden behind their public key.

### Methods Used:

// recover

```commandline
PS:> solana-keygen recover 'prompt:?key=0/0'
```
```commandline
PS:> solana-keygen recover 'prompt:?key=0/1'
```
```commandline
PS:> solana-keygen recover 'prompt:?key=0/2'
```
```commandline
PS:> solana-keygen recover 'prompt:?key=1/0'
```
```commandline
PS:> solana-keygen recover 'prompt:?key=1/1'
```
```commandline
PS:> solana-keygen recover 'prompt:?key=1/2'
```

// pubkey

```commandline
PS:> solana-keygen pubkey prompt://
```
```commandline
PS:> solana-keygen pubkey ASK
```

... All of which do not reflect my actual Wallet Address





## DISCLAIMER: This Repository is a work in progress


