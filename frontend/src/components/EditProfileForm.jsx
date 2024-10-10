import React, { useState, useEffect } from 'react';
import { db, auth } from '../../firebaseConfig';  // Import Firebase config
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { onAuthStateChanged } from 'firebase/auth';
import Swal from 'sweetalert2';

const EditProfileForm = () => {
  const [firebase_uid, setFirebaseUid] = useState('');
  const [message, setMessage] = useState('');
  const [profileData, setProfileData] = useState({
    matric: '',
    name: '',
    email: '',
    usm: '',
    phone: '',
    ic: '',
    course: '',
    birth: '',
    gender: '',
    university: '',
    school: '',
    race: '',
    religion: ''
  });

  // Function to fetch existing profile data from Firestore
  const fetchProfileData = async (uid) => {
    try {
      const docRef = doc(db, "students", uid);
      const docSnap = await getDoc(docRef);

      if (docSnap.exists()) {
        setProfileData(docSnap.data());
        console.log("Existing profile data found:", profileData);
      } else {
        console.log("No existing profile data found.");
      }
    } catch (error) {
      console.error("Error fetching profile data:", error);
    }
  };

  // Get the authenticated user's UID and fetch profile data
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        const uid = user.uid;
        console.log("User is signed in:", uid);
        setFirebaseUid(uid);
        fetchProfileData(uid);  // Fetch the existing profile data
      } else {
        console.log("No user is signed in.");
      }
    });

    return () => unsubscribe();
  }, []);

  // Select University of Science Malaysia, set [University of Science Malaysia, USM, Universiti Sains Malaysia] as the universiti
  const handleUniversityChange = (e) => {
    const selectedUniversity = e.target.value;
        let values = [];

        // Map selected value to an array of names
        if (selectedUniversity === "University of Science Malaysia") {
            values = ["University of Science Malaysia", "Universiti Sains Malaysia", "USM"];
        } else {
            // can use else if to add more universities alternative names
            values = [selectedUniversity];
        }

        setUniversity(values); // Store the array of values
  };

  // Handle the selection of the school
  const handleSchoolChange = (e) => {
    const selectedSchool = e.target.value;
    let values = [];

    // Map selected value to an array of names
    if (selectedSchool === "School of Computer Sciences") {
        values = ["School of Computer Sciences", "Computer Sciences","Sains Komputer"];
    } else if (selectedSchool === "School of Arts") {
        values = ["School of Arts", "Art","Seni"];
    } else if (selectedSchool === "School of Mathematics") {
      values = ["School of Mathematics", "Mathematics","Matematik"];
    } else if (selectedSchool === "School of Management") {
      values = ["School of Management", "Management","Pengurusan"];
    } else {
        // can use else if to add more schools alternative names
        values = [selectedSchool];
    };

    setSchool(values); // Store the array of values
  };

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileData((prevState) => ({
      ...prevState,
      [name]: value
    }));
  };

  // Handle form submission to update data in Firestore
  const handleSubmit = async (e) => {
    e.preventDefault();

    // SweetAlert2 Confirmation
    const confirmation = await Swal.fire({
      title: "Are you sure?",
      text: "Please confirm the updated details.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, update it!",
      cancelButtonText: "Cancel",
    });

    if (confirmation.isConfirmed) {
      try {
        const docRef = doc(db, "students", firebase_uid);
        await setDoc(docRef, profileData, { merge: true });  // Merge true to avoid overwriting

        Swal.fire({
          title: "Success!",
          text: "Profile information updated successfully.",
          icon: "success",
          timer: 2000,
          showConfirmButton: false,
        });
      } catch (error) {
        console.error('Error updating profile:', error);
        Swal.fire({
          title: "Update Failed",
          text: error.message,
          icon: "error",
          timer: 3000,
          showConfirmButton: false,
        });
      }
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
    <div className="bg-white w-full max-w-3xl p-4 border border-gray-300 rounded-md shadow-lg align-items">
    <div className="flex items-center space-x-4 mb-4">
      <h1 className="text-2xl font-bold">Edit Personal Info Form</h1>
    </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 md:gap-x-10">
        {/* Matric Number */}
        <label className="block">
          Matric Number:
          <input
            type="text"
            name="matric"
            value={profileData.matric}
            onChange={handleChange}
            placeholder='1xxxxx'
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Name */}
        <label className="block">
          Name:
          <input
            type="text"
            name="name"
            value={profileData.name}
            onChange={handleChange}
            placeholder="JOHN DOE"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* IC Number */}
        <label className="block">
          IC Number:
          <input
            type="text"
            name="ic"
            value={profileData.ic}
            onChange={handleChange}
            placeholder="xxxxxx-xx-xxxx"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Course */}
        <label className="block">
          Course:
          <input
            type="text"
            name="course"
            value={profileData.course}
            onChange={handleChange}
            placeholder="COMPUTER SCIENCES"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Birthday */}
        <label className="block">
          Birthday:
          <input
            type="date"
            name="birth"
            value={profileData.birth}
            onChange={handleChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Gender */}
        <label className="block">
          Gender:
          <select
            name="gender"
            value={profileData.gender}
            onChange={handleChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </label>

        {/* Phone */}
        <label className="block">
          Phone:
          <input
            type="tel"
            name="phone"
            value={profileData.phone}
            onChange={handleChange}
            placeholder="+6012-3456789"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Email */}
        <label className="block">
          Personal Email:
          <input
            type="email"
            name="email"
            value={profileData.email}
            onChange={handleChange}
            placeholder="johndoe@gmail.com"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* USM Email */}
        <label className="block">
          USM Email:
          <input
            type="email"
            name="usm"
            value={profileData.usm}
            onChange={handleChange}
            placeholder="johndoe@student.usm.my"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* University */}
        <label className="block">
          University:
          <select
            name="university"
            value={profileData.university[0] || ''} 
            onChange={handleUniversityChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select University</option>
            <option value="University of Science Malaysia">University of Science Malaysia</option>
          </select>
        </label>

        {/* School */}
        <label className="block">
          School:
          <select
            name="school"
            value={profileData.school[0] || ''}
            onChange={handleSchoolChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select School</option>
            <option value="School of Arts">School of Arts</option>
            <option value="School of Computer Sciences">School of Computer Sciences</option>
            <option value="School of Mathematics">School of Mathematics</option>
            <option value="School of Management">School of Management</option>
          </select>
        </label> 

        {/* Race */}
        <label className="block">
          Race:
          <select
            name="school"
            value={profileData.race}
            onChange={handleChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select Race</option>
            <option value="Chinese">Chinese</option>
            <option value="Malay">Malay</option>
            <option value="Indian">Indian</option>
          </select>
        </label>

        {/* Religion */}
        <label className="block">
          Religion:
          <select
            name="religion"
            value={profileData.religion}
            onChange={handleChange}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select Religion</option>
            <option value="Islam">Islam</option>
            <option value="Christianity">Christianity</option>
            <option value="Buddhism">Buddhism</option>
            <option value="Hinduism">Hinduism</option>
            <option value="Others">Others</option>
          </select>
        </label>

        {/* col-span-2 makes the element to take up two columns of the parent container if the container uses grid-cols-n */}
        <button
          type="submit"
          className="col-span-2 bg-blue-500 text-white p-2 rounded w-full mt-6"
        >
          Update
        </button>
      </form> 

      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
    </div>
  );
};

export default EditProfileForm;