
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";

import {
    getAuth,
    setPersistence,
    browserLocalPersistence
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

import {
    getDatabase
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyAUHdrCJNOeK5ONFtkIbfkc4p7UQcOkNwE",
    authDomain: "smart-waste-management-7d746.firebaseapp.com",
    databaseURL: "https://smart-waste-management-7d746-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "smart-waste-management-7d746",
    storageBucket: "smart-waste-management-7d746.firebasestorage.app",
    messagingSenderId: "818207531595",
    appId: "1:818207531595:web:627515ef786263c1a1e3ce",
    measurementId: "G-SD3CBQKKNV"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const database = getDatabase(app);

export const authReady = setPersistence(
    auth,
    browserLocalPersistence
);
