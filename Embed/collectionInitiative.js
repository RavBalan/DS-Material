const express = require("express")
const { ChromaClient } = require("chromadb");



const app = express();
app.use(express.json());

const client = new ChromaClient({
    host: "dev1.baas360.alitasys.com",
    port: 7017,
    // ssl: false,
    // headers: {
    //     "Authorization":
    //         "Basic " + Buffer.from("devadmin:GuthFFTNK092&").toString("base64"),
    // },
});

app.get("/checkconnection", async (req, res) => {
    try {
        const hb = await client.heartbeat();
        res.json({ status: "alive", heartbeat: hb });
    } catch (error) {
        console.error("Heartbeat error:", error.message);
        res.status(500).json({ error: "Failed to reach Chroma server" });
    }
});

app.post("/listcollection", async (req, res) => {
    try {
        const collections = await client.listCollections();
        console.log("Collections:", collections);
        res.json({ collections });
    } catch (error) {
        console.error("Error listing collections:", error.message);
        res.status(500).json({ error: error.message });
    }
});

app.post("/createcollection", async (req, res) => {
    const { name } = req.body;
    if (!name)
        return res.status(400).json({ error: "Collection name is required" });

    try {
        const newCollection = await client.createCollection({ name });
        console.log("Collection created:", newCollection);
        res.json({ message: "Collection created", newCollection });
    } catch (error) {
        console.error("Error creating collection:", error.message);
        res.status(500).json({ error: error.message });
    }
});
app.delete("/deletecollection", async (req, res) => {
    const { name } = req.body;

    if (!name) {
        return res.status(400).json({ error: "Collection name is required" });
    }
    try {
        await client.deleteCollection({ name: name });

        console.log(`Deleted collection: ${name}`);
        res.json({ message: `Collection '${name}' deleted successfully.` });
    } catch (error) {
        console.error("Error deleting collection:", error.message);
        res.status(500).json({ error: error.message });
    }
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
