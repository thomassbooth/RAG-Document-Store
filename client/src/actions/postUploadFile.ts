/**
 * Function to call nextjs api to upload a file
 * @param formData File form data
 * @returns an error or if its ok
 */
export const upload_file = async (formData: FormData) => {
  const LOCAL_URL = process.env.NEXT_PUBLIC_LOCAL_URL;
  const res = await fetch(`${LOCAL_URL}/api/upload`, {
    // replace with your FastAPI URL
    method: "POST",
    body: formData,
  });

  return res;
};
