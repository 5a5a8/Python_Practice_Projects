import hashlib
import json
import requests
import time

from flask import Flask, jsonify, request
from textwrap import dedent
from urllib.parse import urlparse
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        #create the genesis block
        self.new_block(proof=100, prev_hash=1)

    def register_node(self, address):
        """adds a new node to the list of nodes.
        address is a string with the address of the node"""

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, prev_hash=None):
        """Create a new block on the chain including the current transactions."""

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash or self.hash_block(self.chain[-1]),
        }

        #block created so we no longer need all the transactions
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender, receiver, amount):
        """Creates a new transaction to go into the next mined block by 
        appending a dictionary of the {sender, receiver, amount} to the
        current transactions and then returning the index of the next
        block to be mined"""

        self.current_transactions.append({
                'sender': sender,
                'receiver': receiver,
                'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash_block(block):
        block_str = json.dumps(block, sort_keys=True)
        sha256hash = hashlib.sha256(block_str.encode()).hexdigest()
        return sha256hash

    @property
    def last_block(self):
        return self.chain[-1]


    def proof_of_work(self, prev_proof):
        """This function implements the proof of work algorith which is:
            -find a number p' such that hash(pp') has N=4 leading zeroes
            -p is the previous p'
            -pp' is like {prev_proof}{proof}"""

        #we simply iterate until our proof is valid
        proof = 0
        while not self.valid_proof(prev_proof, proof, work_difficulty=4):
            proof += 1

        return proof


    @staticmethod
    def valid_proof(prev_proof, proof, work_difficulty):
            """Checks if the proof is valid. 
            e.g. checks the hash of prev_proof and proof contains
            N=4 leading zeroes"""

            guess = f'{prev_proof}{proof}'
            guess_hash = hashlib.sha256(guess.encode()).hexdigest()
            
            #if the first N digits are zeroes, our proof is valid
            return guess_hash[:work_difficulty] == '0' * work_difficulty

    def valid_chain(self, chain):
        """determine if a given blockchain is valid"""

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n----------\n')

            #check that the hash is correct
            if block['prev_hash'] != self.hash_block(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], 4):
                return False

            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """The longest valid chain is seen as the source of truth.
        If there are any chain conflicts between the different nodes,
        we simply select the longest valid one.
        Return true if our chain was replaced."""

        neighbours = self.nodes
        new_chain = None

        #we don't care about nodes shorter than ours
        max_len = len(self.chain)

        #look for the longest valid chain
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_len and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        #replace our chain with the longest valid one we found
        if new_chain:
            self.chain = new_chain
            return True

        return False


"""we use flask to set everything up so we can interact via HTTP
we will create three methods:
    -/mine to mine a new block
    -/transactions/new to create a new transaction on the block
    -/chain to return the entire blockchain"""

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #we must receive a reward for mining
    #sender is 0 to indicate transaction is from mining
    blockchain.new_transaction(
        sender = '0',
        receiver = node_identifier,
        amount = 1
    )

    #add the newly mined block to the chain
    prev_hash = blockchain.hash_block(last_block)
    block = blockchain.new_block(proof, prev_hash)

    response = {
        'message': 'New block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['prev_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    #check all required fields are present in the POST request
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values, required: sender, recipient, amount', 400

    #create a new transaction on the next block
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return 'Error: Please supply a valid list of nodes', 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes added successfully',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

