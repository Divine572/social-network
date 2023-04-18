from flask import Flask, render_template, request
from web3 import Web3
import os
import deploy

w3 = deploy.w3

abi = deploy.abi
contract_address = deploy.contract_address
deployer = deploy.deployer

# Define the Flask app
app = Flask(__name__, template_folder='templates')

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)


# # Define the Flask routes
# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/create-user', methods=['POST'])
def create_user():
    username = request.form['username']
    tx_hash = contract.functions.createUser(
        username).transact({'from': deployer})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return 'User created successfully'


@app.route('/create-post', methods=['POST'])
def create_post():
    content = request.form['content']
    tx_hash = contract.functions.createPost(
        content).transact({'from': deployer})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return 'Post created successfully'


@app.route('/posts')
def posts():
    post_count = contract.functions.getPostCount().call()
    posts = []
    for i in range(post_count):
        post = contract.functions.getPost(i).call()
        posts.append(post)
    return render_template('posts.html', posts=posts)


# Run the Flask app
if __name__ == '__main__':
    app.run()
