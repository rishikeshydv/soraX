import {initializeApp} from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "@firebase/firestore";   //this is for the cloud firestore
//import { getDatabase } from "firebase/database";    // this is for the realtime database
import dotenv from 'dotenv';
dotenv.config(); 
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAo3713_3WLW5I65VvVxpfrLtT_0bKhvrY",
  authDomain: "sorax-e0803.firebaseapp.com",
  projectId: "sorax-e0803",
  storageBucket: "sorax-e0803.appspot.com",
  messagingSenderId: "373452001436",
  appId: "1:373452001436:web:7ec8db05628adb75149d59",
  measurementId: "G-MNW5SDTNQE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
//const realtimeDatabase = getDatabase(app);
export {app,auth,db}