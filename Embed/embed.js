const { DefaultEmbeddingFunction } = require("@chroma-core/default-embed")
const { ChromaClient } = require("chromadb");


const defaultEF = new DefaultEmbeddingFunction();

async function embedder(data) {
  try {
    const embeddings = await defaultEF.generate(data);
    console.log(JSON.stringify(embeddings));
  } catch (error) {

  }
}

embedder([
  "Python is a high-level programming language.",
  "Node.js allows running JavaScript on the server.",
  "ChromaDB is a vector database for embeddings and semantic search."
])


[{
    "_id": {
      "$oid": "68199b367e1be31366105998"
    },
    "DocumentBillID": 138542,
    "PlateNumber": 3264531,
    "PlateState": "IN",
    "PlateCountry": "USA",
    "BillNumber": 30990431,
    "BillDate": {
      "$date": "2025-04-01T00:00:00.000Z"
    },
    "BillType": "TOLL",
    "NoticeType": "Second",
    "VendorCode": "OK-PIKEPASS",
    "TotalTransactionAmount": 0,
    "TotalFeeAmount1": 0,
    "PaymentStatus": "NO DUE",
    "PlateStatus": 1,
    "PlateStartDate": "5/6/2025",
    "PlateEndDate": null
  }]