/**
 * Represents a node in the prefix tree.
 */
class TrieNode {
    /**
     * Initializes a new TrieNode instance.
     */
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
    }
}

/**
 * Prefix tree (Trie) for efficient string retrieval.
 */
class Trie {
    /**
     * Initializes an empty Trie with a root node.
     */
    constructor() {
        this.root = new TrieNode();
    }

    /**
     * Inserts a word into the trie.
     *
     * @param {string} [word=''] - The string to insert.
     */
    insert(word = '') {
        let current = this.root;
        for (const char of word) {
            if (!current.children[char]) {
                current.children[char] = new TrieNode();
            }
            current = current.children[char];
        }
        current.isEndOfWord = true;
    }

    /**
     * Searches for a complete word in the trie.
     *
     * @param {string} [word=''] - Word to search for.
     * @returns {boolean} True if the word exists in the trie.
     */
    search(word = '') {
        let current = this.root;
        for (const char of word) {
            if (!current.children[char]) {
                return false;
            }
            current = current.children[char];
        }
        return current.isEndOfWord;
    }

    /**
     * Checks if there is any word in the trie that starts with the given prefix.
     *
     * @param {string} [prefix=''] - Prefix to look up.
     * @returns {boolean} True if prefix exists.
     */
    startsWith(prefix = '') {
        let current = this.root;
        for (const char of prefix) {
            if (!current.children[char]) {
                return false;
            }
            current = current.children[char];
        }
        return true;
    }
}

module.exports = { TrieNode, Trie };
