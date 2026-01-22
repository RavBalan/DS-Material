// const HF_API_KEY = "";

const axios = require("axios");
const { ChromaClient } = require("chromadb");
const client = new ChromaClient({
    host: "http://dev1.baas360.alitasys.com:7017",
    // Username: "devadmin",
    // Password: "GuthFFTNK092&"

});

async function getEmbedding(texts) {
    const embeddings = [];
    for (const text of texts) {
        const response = await axios.post(
            "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
            { inputs: text },
            {
                headers: {
                    Authorization: `Bearer `,
                    "Content-Type": "application/json"
                }
            }
        );
        embeddings.push(response.data[0]);
    }
    console.log(embeddings);
    return embeddings;
}
getEmbedding([
    "Python is a high-level programming language.",
    "Node.js allows running JavaScript on the server.",
    "ChromaDB is a vector database for embeddings and semantic search."
])

// async function main() {
//   const collection = await client.getOrCreateCollection({ name: "my_collection" });

//   const documents = [
//     "Python is a high-level programming language.",
//     "Node.js allows running JavaScript on the server.",
//     "ChromaDB is a vector database for embeddings and semantic search."
//   ];

//   const embeddings = await getEmbedding(documents);

//   await collection.add({
//     ids: documents.map((_, i) => `doc${i}`),
//     documents,
//     embeddings
//   });

//   console.log("✅ Documents stored in ChromaDB");

//   const queryEmbedding = await getEmbedding(["What is ChromaDB?"]);
//   const results = await collection.query({
//     queryEmbeddings: queryEmbedding,
//     nResults: 2
//   });

//   console.log("\n🔎 Search results:");
//   results.documents[0].forEach((doc, idx) => {
//     console.log(`Result ${idx + 1}: ${doc}`);
//   });
// }

// main();