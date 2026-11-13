class TrieGodClass {
    constructor() {
        this.root = {};
        this.exportPath = "/tmp/trie_dump.json";
        this.delimiter = ",";
        this.logBuffer = [];
        this.logLevel = "INFO";
        this.metrics = [];
        this.cache = {};
        this.stopWords = new Set();
    }

    insert(word) {
        let node = this.root;
        for (let i = 0; i < word.length; i++) {
            let ch = word[i];
            if (!node[ch]) {
                node[ch] = {};
            }
            node = node[ch];
        }
        node.$ = true;
    }

    search(word) {
        let node = this.root;
        for (let i = 0; i < word.length; i++) {
            let ch = word[i];
            if (!node[ch]) {
                return false;
            }
            node = node[ch];
        }
        return node.$ === true;
    }

    setExportPath(path) {
        this.exportPath = path;
    }

    setDelimiter(delim) {
        this.delimiter = delim;
    }

    dumpToJson() {
        return JSON.stringify({ path: this.exportPath, tree: this.root });
    }

    exportToCsv(records) {
        let lines = [];
        for (let i = 0; i < records.length; i++) {
            lines.push(records[i].join(this.delimiter));
        }
        return lines.join("\n");
    }

    logOperation(msg) {
        let entry = "[" + this.logLevel + "] " + msg;
        this.logBuffer.push(entry);
    }

    dumpLogBuffer() {
        return this.logBuffer.slice();
    }

    clearLogs() {
        this.logBuffer = [];
    }

    recordLatency(ms) {
        this.metrics.push(ms);
    }

    getAverageLatency() {
        if (this.metrics.length === 0) {
            return 0;
        }
        let sum = 0;
        for (let i = 0; i < this.metrics.length; i++) {
            sum += this.metrics[i];
        }
        return sum / this.metrics.length;
    }

    evictCache(key) {
        delete this.cache[key];
    }

    addStopWord(word) {
        this.stopWords.add(word);
    }

    isStopWord(word) {
        return this.stopWords.has(word);
    }

    filterText(tokens) {
        let out = [];
        for (let i = 0; i < tokens.length; i++) {
            if (!this.stopWords.has(tokens[i])) {
                out.push(tokens[i]);
            }
        }
        return out;
    }
}

module.exports = { TrieGodClass };
