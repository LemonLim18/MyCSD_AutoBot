// src/components/Form.jsx
// THIS IS THE FORM COMPONENT USED BY NEW PROFILE INFO PAGE & EDIT PROFILE INFO PAGE
import React, { useState } from 'react';
import { Tooltip, Button } from 'antd';
import Swal from 'sweetalert2';
import { db } from '../../firebaseConfig';
import { collection, addDoc } from 'firebase/firestore';

const Form = () => {
  const [matricNumber, setMatricNumber] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [usmEmail, setUsmEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [ic, setIc] = useState('');
  const [course, setCourse] = useState('');
  const [birthday, setBirthday] = useState('');
  const [gender, setGender] = useState('');
  const [university, setUniversity] = useState('');
  const [school, setSchool] = useState('');
  const [race, setRace] = useState('');
  const [religion, setReligion] = useState('');
  const [message, setMessage] = useState('');
  // const [isBotRunning, setIsBotRunning] = useState(false);

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      name: name,
      matric: matricNumber,
      ic: ic,
      phone: phone,
      email: email,
      usm_email: usmEmail,
      course: course,
      school: school,
      birth: birthday,
      gender: gender,
      race: race,
      religion: religion,
      university: university,
    };

    console.log('Submitting form with data:', data);  // Log data to console

    // SweetAlert2 Confirmation Dialog
    const confirmation = await Swal.fire({
      title: "Are you sure?",
      text: "Please confirm the details. You are still able to update the information afterwards.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, submit it!",
      cancelButtonText: "Cancel",
      // confirmButtonColor: "#d33", // Red color for "dangerous" actions
      // cancelButtonColor: "#3085d6", // Default color for cancel button
    });
    
    // db: database; collection: table; document: entry(with id and data[key-pair values])
    if (confirmation.isConfirmed) {
        // Try submitting the form
      try {
        // Push the data to the Firestore first, then allow the backend server to collect the data on our commands
        const docRef = await addDoc(collection(db, "students"), data);
        // docRef refers to the document
        console.log("Document written with ID: ", docRef.id);

        // Display a success message
        Swal.fire({
          title: "Success!",
          text: `Document successfully written with ID: ${docRef.id}`,
          icon: "success",
          timer: 2000,
          showConfirmButton: false, // No buttons in the success alert
        }).then(() => {
          // Returning to the login page
          Swal.fire({
            title: "Returning to login page...",
            html: "Please wait <b></b> seconds.",
            timer: 3000,
            timerProgressBar: true,
            allowOutsideClick: false,
            didOpen: () => {
              const b = Swal.getHtmlContainer().querySelector("b");
              Swal.showLoading();
              const interval = setInterval(() => {
                b.textContent = Math.ceil(Swal.getTimerLeft() / 1000);
              }, 100);
            },
            willClose: () => {
              // Redirect to login page after timer ends
              window.location.href = "/login";
            }
          });
        });

        // Optionally, send the data straight to the backend server
        // const response = await fetch('http://127.0.0.1:5000/submit-form', {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify(data),
        // });
        // if (!response.ok) {
        //   const errorMessage = `Server responded with status: ${response.status} - ${response.statusText}`;
        //   throw new Error(errorMessage);
        // }
        // const result = await response.json();
        // setMessage(result.message);
        // // SweetAlert2 Success Alert
        // Swal.fire({
        //   title: "Success!",
        //   text: result.message,
        //   icon: "success",
        //   timer: 3400,
        //   showConfirmButton: false, // No buttons in the success alert
        // });

        // Delay before redirecting (e.g., 2 seconds)
        // setTimeout(() => {
        //   window.location.href = "/login"; // Replace with your redirect URL
        // }, 3400);
      } catch (error) {
        console.error('Error submitting form:', error);
        // SweetAlert2 Error Alert
        Swal.fire({
          title: "Submission Failed!",
          text: error.message || 'An error occurred while submitting the form.',
          icon: "error",
          timer: 3000,
          showConfirmButton: false, // No buttons in the error alert
        });
      }
    } else {
        Swal.fire("Form submission canceled!", {
          icon: "info",
          timer: 1500,
          showConfirmButton: false,
        });
    }
  };


    
    // } catch (error) {
    //   console.error('Error submitting form:', error);
    //   // Provide a more specific message if the error is network-related
    //   if (error.name === 'TypeError') {
    //     setMessage('Network error: Unable to reach the server. Please try again later.');
    //   } else {
    //     setMessage('Error submitting form');
    //   }
    // }


  // ROBOT ACTIVATION BUTTON - COMMENT FOR NOW
  // Activate the Bot
  // const handleStartBot = async () => {
  //   console.log('Starting bot...');  // Log bot start action
  //   try {
  //     const response = await fetch('http://127.0.0.1:5000/start-bot', {
  //       method: 'POST',
  //     });

  //     const result = await response.json();
  //     console.log('Response from start-bot:', result);  // Log response from start-bot

  //     if(response.ok) {
  //       setIsBotRunning(true);  // Set isBotRunning to true if the bot is started successfully
  //     }
  //     setMessage(result.message);
  //   } catch (error) {
  //     console.error('Error starting bot:', error);
  //     setMessage('Error starting bot');
  //   }
  // };

  // // Deactivate the Bot
  // const handleStopBot = async () => {
  //   console.log('Stopping bot...');  // Log bot stop action
  //   try {
  //     const response = await fetch('http://127.0.0.1:5000/stop-bot', {
  //       method: 'POST',
  //     });

  //     const result = await response.json();
  //     console.log('Response from stop-bot:', result);  // Log response from stop-bot

  //     if(response.ok) {
  //       setIsBotRunning(false);  // Set isBotRunning to false if the bot is stopped successfully
  //     }
  //     setMessage(result.message);
  //   } catch (error) {
  //     console.error('Error stopping bot:', error);
  //     setMessage('Error stopping bot');
  //   }
  // };
 
  return (
    <div className="flex items-center justify-center h-screen">
    <div className="bg-white w-full max-w-3xl p-4 border border-gray-300 rounded-md shadow-lg align-items">
    <div className="flex items-center space-x-4 mb-4">
      <h1 className="text-2xl font-bold">Personal Info Form</h1>
      <Tooltip className="top-[2.5px] rounded-3xl" title="This form is used to store the information to be automatically filled into the GForm. You may update the information afterwards as well.">
        <Button>?</Button>
      </Tooltip>
    </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 md:gap-x-10">
        {/* Matric Number */}
        <label className="block">
          Matric Number:
          <input
            type="text"
            value={matricNumber}
            onChange={(e) => setMatricNumber(e.target.value)}
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
            value={name}
            onChange={(e) => setName(e.target.value)}
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
            value={ic}
            onChange={(e) => setIc(e.target.value)}
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
            value={course}
            onChange={(e) => setCourse(e.target.value)}
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
            value={birthday}
            onChange={(e) => setBirthday(e.target.value)}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* Gender */}
        <label className="block">
          Gender:
          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
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
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
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
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            value={usmEmail}
            onChange={(e) => setUsmEmail(e.target.value)}
            placeholder="johndoe@student.usm.my"
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* University */}
        <label className="block">
          University:
          <select
            value={university[0] || ''} 
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
            value={school[0] || ''}
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
            value={race}
            onChange={(e) => setRace(e.target.value)}
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
            value={religion}
            onChange={(e) => setReligion(e.target.value)}
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
          Submit
        </button>
      </form>

      {/* ROBOT ACTIVATION BUTTON - COMMENT FOR NOW */}
      {/* <button
        onClick={isBotRunning ? handleStopBot : handleStartBot}
        className={`text-white p-2 rounded w-full mt-2 ${isBotRunning ? 'bg-red-500':'bg-green-500'}`}
      >
        {isBotRunning ? 'Stop Bot' : 'Start Bot'}
      </button> */}

      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
    </div>
  );
};

export default Form;