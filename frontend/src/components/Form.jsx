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

      const result = await response.json();
      console.log('Response from server:', result);  // Log response from server
      setMessage(result.message);
    } catch (error) {
      console.error('Error submitting form:', error);
      setMessage('Error submitting form');
    }
  };

  const handleStartBot = async () => {
    console.log('Starting bot...');  // Log bot start action
    try {
      const response = await fetch('http://127.0.0.1:5000/start-bot', {
        method: 'POST',
      });

      const result = await response.json();
      console.log('Response from start-bot:', result);  // Log response from start-bot
      setMessage(result.message);
    } catch (error) {
      console.error('Error starting bot:', error);
      setMessage('Error starting bot');
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
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* University */}
        <label className="block">
          University:
          <select
            value={university}
            onChange={(e) => setUniversity(e.target.value)}
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
            value={school}
            onChange={(e) => setSchool(e.target.value)}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          >
            <option value="">Select School</option>
            <option value="School of Computer Sciences">School of Computer Sciences</option>
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
          <input
            type="text"
            value={religion}
            onChange={(e) => setReligion(e.target.value)}
            required
            className="mt-1 p-2 border border-gray-300 rounded w-full"
          />
        </label>

        {/* col-span-2 makes the element to take up two columns of the parent container if the container uses grid-cols-n */}
        <button
          type="submit"
          className="col-span-2 bg-blue-500 text-white p-2 rounded w-full mt-4"
        >
          Submit
        </button>
      </form>
      <button
        onClick={handleStartBot}
        className="bg-green-500 text-white p-2 rounded w-full mt-4"
      >
        Start Bot
      </button>
      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
    </div>
  );
};

export default Form;