// components/FileUpload.js
import { useState } from "react";
import { Button } from "./ui/button";
import { upload_file } from "@/actions/postUploadFile";

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
      
      const res = await upload_file(formData)
      
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
      <Button onClick={handleUpload}>Upload</Button>
      {status && <p>{status}</p>}
    </div>
  );
};

export default FileUpload;
