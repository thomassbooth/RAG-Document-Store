// components/FileUpload.js
import { useState } from "react";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  //@ts-expect-error // ignore type error
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // append the selected file to the formData

    try {
      const res = await fetch("http://localhost:8000/upload", { // replace with your FastAPI URL
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        setStatus("File uploaded successfully!");
      } else {
        setStatus("File upload failed.");
      }
    } catch (err) {
      console.error("Error uploading file:", err);
      setStatus("An error occurred while uploading the file.");
    }
  };

  return (
    <div>
      <h1>Upload a File</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {status && <p>{status}</p>}
    </div>
  );
};

export default FileUpload;
