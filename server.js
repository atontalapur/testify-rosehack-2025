const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
const uploadDir = path.join(__dirname, "uploads");

// Ensure uploads folder exists
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
  console.log(`Created uploads folder at ${uploadDir}`);
}

const upload = multer({
  dest: "uploads/",
  fileFilter: (req, file, cb) => {
    const allowedTypes = ["application/pdf", "application/zip"];
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error("Only .pdf and .zip files are allowed"));
    }
    cb(null, true);
  },
});

// Serve static files from PreWorkshop/public
app.use(express.static(path.join(__dirname, "PreWorkshop")));

// File upload endpoint
app.post("/upload", upload.array("files"), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: "No files uploaded" });
  }

  console.log("Uploaded Files:", req.files); // Debug uploaded files
  res.json({ message: "Files uploaded successfully!", files: req.files });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

app.post("/upload", upload.array("files"), (req, res) => {
  console.log("Request received:", req.body);
  console.log("Uploaded Files:", req.files);

  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: "No files uploaded" });
  }

  res.json({ message: "Files uploaded successfully!", files: req.files });
});
