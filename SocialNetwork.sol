// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SocialNetwork {
    struct Post {
        address author;
        string content;
        uint timestamp;
    }
    
    mapping(address => string) public users;
    Post[] public posts;
    
    function createUser(string memory username) public {
        users[msg.sender] = username;
    }
    
    function createPost(string memory content) public {
        require(bytes(users[msg.sender]).length != 0, 'User does not exist');
        Post memory post = Post(msg.sender, content, block.timestamp);
        posts.push(post);
    }
    
    function getPost(uint index) public view returns (address, string memory, uint) {
        require(index < posts.length, 'Invalid post index');
        Post memory post = posts[index];
        return (post.author, post.content, post.timestamp);
    }
    
    function getPostCount() public view returns (uint) {
        return posts.length;
    }
}
