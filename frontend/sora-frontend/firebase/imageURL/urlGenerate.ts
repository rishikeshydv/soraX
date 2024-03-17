
import firebase from "firebase/app";
import { getStorage, ref, uploadBytes,getDownloadURL } from "firebase/storage";

const uploadVideo = async (video: File) => {
  // Initialize Firebase Storage
  const storage = getStorage();

  // Create a reference to the upload location
  const storageRef = ref(storage,"generated_video");

  fetch('/get_video')
  .then(response => {
      if (!response.ok) {
          throw new Error('Could not fetch the video');
      }
    return response.blob();
  })
  .then(blob => {
    uploadBytes(storageRef, blob)
  .then((snapshot) => {
    getDownloadURL(storageRef).then((downloadURL) => {
      console.log('File available at', downloadURL);
      // Send the downloadURL to the backend
      //write a logic to send this url to the videoGenerated Prop in the frontend of nextjs
    });
    });
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  });
};
