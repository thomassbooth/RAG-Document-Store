
/**
 * Function to call nextjs api to upload a file
 * @param formData File form data
 * @returns an error or if its ok
 */
export const upload_file = async (formData: FormData) => {

    console.log("upload_file")
  const res = await fetch(`http://localhost:3001/api/upload`, {
    // replace with your FastAPI URL
    method: "POST",
    body: formData,
  });

  return res
};
