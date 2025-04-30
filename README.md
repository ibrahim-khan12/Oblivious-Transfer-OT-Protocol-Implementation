# 🛡️ Privacy-Preserving Auction System  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A secure auction system built on cryptographic protocols, specifically implementing the **Naor-Pinkas 1-out-of-2 Oblivious Transfer (OT)** protocol to preserve bidder privacy while ensuring fair and verifiable auction outcomes.

---

## 📚 Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [System Architecture](#system-architecture)  
- [Security Properties](#security-properties)  
- [Development](#development)  
- [Contributors](#contributors)  
- [License](#license)  

---

## 🔍 Overview

This project implements a **privacy-preserving auction system** using cryptographic techniques to protect sensitive bidder information while guaranteeing fairness. The core mechanism is the **Naor-Pinkas 1-out-of-2 Oblivious Transfer (OT)** protocol, enabling secure communication in which a sender offers two messages and the receiver retrieves only one—without revealing their choice.

---

## ✨ Features

- 🔒 **Secure Bidding**: Participants submit bids privately—values remain hidden until the end.
- ✍️ **Bid Authentication**: Digital signatures ensure the integrity of each bid and provide non-repudiation.
- 🧾 **Verifiable Results**: All participants can independently verify the auction outcome.
- 🕵️ **Privacy Preservation**: Neither bid values nor bidder identities are exposed.
- ⚙️ **Flexible Parameters**: Supports configurable auction duration and participant limits.
- 🔐 **Cryptographically Sound**: Built using robust, well-established cryptographic primitives.

---

## ⚙️ Technology Stack

### 🖥️ Programming Language
- **Python 3.8+**

### 🔐 Cryptographic Components
- **Naor-Pinkas 1-out-of-2 Oblivious Transfer**
- **2048-bit MODP Group** (RFC 3526)
- **AES-GCM** for authenticated symmetric encryption
- **SHA-256** hashing
- **ECDSA** signatures (SECP256R1 curve)

### 📦 Libraries Used
- [`cryptography`](https://cryptography.io/) – Python cryptographic toolkit

---

## 🧰 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ibrahim-khan12/privacy-auction.git
   cd privacy-auction
   ```
   ▶️ Usage
🧪 Running a Demo Auction
To simulate an example auction involving three participants (Alice, Bob, and Charlie):

bash
Copy
Edit
python demo_auction.py
This will:

✅ Register each bidder

✅ Collect and verify bids

✅ Preserve privacy via OT

✅ Reveal and verify the winning bid at the end

## System Architecture
🧩 Key Components
SecureAuction
Orchestrates registration, bidding, verification, and finalization.

Auctioneer
Manages bid collection, validation via OT, and result computation.

Bidder
Represents participants; handles bid commitment, proof, and submission.

OT Protocol (auction_ot.py)
Implements the Naor-Pinkas Oblivious Transfer mechanism for secure selection.

🔄 Auction Workflow
Registration Phase

Bidders register and commit to bid values (signed commitments)

Bidding Phase

Bidders submit their encrypted bids using the OT protocol

Verification Phase

Auctioneer verifies authenticity and validity of the bids

Conclusion Phase

Results are calculated, winner is revealed, and all proofs are logged

## Security Properties
🕶️ Bid Privacy
Bid values are encrypted and revealed only after the auction ends.

🛡️ Bid Integrity
Each bid is signed to prevent tampering or replay attacks.

🧾 Non-repudiation
Bidders cannot deny submitted bids due to cryptographic evidence.

📜 Verifiability
All participants can independently validate the correctness of the result.

⏱️ Timing Protections
Constant-time cryptographic operations minimize side-channel risks.

## Development
✅ Running Tests
The project includes test scripts to validate core functionality of:

✔️ Oblivious Transfer

✔️ Signature generation and verification

✔️ End-to-end secure auction simulation

To run the test suite:

bash
Copy
Edit
python test_suite.py
 ## Contributors
This project was developed as part of an Information Security course assignment.

🎓 Ibrahim Khan 

🎓 Asad Khurshid

🎓 Etisham Dhanyal


