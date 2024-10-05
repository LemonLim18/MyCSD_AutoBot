// src/components/Form.jsx
import React, { useState } from 'react';

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
  const [isBotRunning, setIsBotRunning] = useState(false);

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
      matric_number: matricNumber,
      name: name,
      email: email,
      usm_email: usmEmail,
      phone: phone,
      ic: ic,
      course: course,
      birthday: birthday,
      gender: gender,
      university: university,
      school: school,
      race: race,
      religion: religion,
    };

    console.log('Submitting form with data:', data);  // Log data to console

    try {
      const response = await fetch('http://127.0.0.1:5000/submit-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      // Check if the response is ok (status in the range 200-299)
      if (!response.ok) {
        const errorMessage = `Server responded with status: ${response.status} - ${response.statusText}`;
        console.error(errorMessage);
        setMessage(errorMessage);
        return; // Exit early if the response is not ok
      }
    
      const result = await response.json();
      console.log('Status code:', response.status);  // Log status code
      console.log('Response from server:', result);  // Log response from server
      setMessage(result.message);
    } catch (error) {
      console.error('Error submitting form:', error);
      // Provide a more specific message if the error is network-related
      if (error.name === 'TypeError') {
        setMessage('Network error: Unable to reach the server. Please try again later.');
      } else {
        setMessage('Error submitting form');
      }
    }
  };


  // Activate the Bot
  const handleStartBot = async () => {
    console.log('Starting bot...');  // Log bot start action
    try {
      const response = await fetch('http://127.0.0.1:5000/start-bot', {
        method: 'POST',
      });

      const result = await response.json();
      console.log('Response from start-bot:', result);  // Log response from start-bot

      if(response.ok) {
        setIsBotRunning(true);  // Set isBotRunning to true if the bot is started successfully
      }
      setMessage(result.message);
    } catch (error) {
      console.error('Error starting bot:', error);
      setMessage('Error starting bot');
    }
  };

  // Deactivate the Bot
  const handleStopBot = async () => {
    console.log('Stopping bot...');  // Log bot stop action
    try {
      const response = await fetch('http://127.0.0.1:5000/stop-bot', {
        method: 'POST',
      });

      const result = await response.json();
      console.log('Response from stop-bot:', result);  // Log response from stop-bot

      if(response.ok) {
        setIsBotRunning(false);  // Set isBotRunning to false if the bot is stopped successfully
      }
      setMessage(result.message);
    } catch (error) {
      console.error('Error stopping bot:', error);
      setMessage('Error stopping bot');
    }
  };
 
  return (
    <div className="flex items-center justify-center h-screen">
    <div className="w-full max-w-3xl p-4 border border-gray-300 rounded shadow-lg align-items">
      <h1 className="text-2xl font-bold mb-4">Personal Info Form</h1>
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
      <button
        onClick={isBotRunning ? handleStopBot : handleStartBot}
        className={`bg-${isBotRunning ?'red':'green'}-500 text-white p-2 rounded w-full mt-2`}
      >
        {isBotRunning ? 'Stop Bot' : 'Start Bot'}
      </button>
      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
    </div>
  );
};

export default Form;