import React, { useState } from 'react';
import Swal from 'sweetalert2';

const Dashboard = () => {
    const [isBotRunning, setIsBotRunning] = useState(false);
    // const [message, setMessage] = useState('');

    // Function to handle the Start Bot button
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
          Swal.fire({
            icon: 'success',
            title: 'Bot Started',
            text: result.message || 'The bot has been started successfully.',
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Error Starting Bot',
            text: result.message || 'Failed to start the bot. Please try again.',
          });
        }
        // setMessage(result.message);
      } catch (error) {
        console.error('Error starting bot:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error Starting Bot',
          text: 'Failed to start the bot. Please try again.',
        });
        // setMessage('Error starting bot');
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
          Swal.fire({
            icon: 'success',
            title: 'Bot Stopped',
            text: result.message || 'The bot has been stopped successfully.',
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Error Stopping Bot',
            text: result.message || 'Failed to stop the bot. Please try again.',
          });
        }
        // setMessage(result.message);
      } catch (error) {
        console.error('Error stopping bot:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error Stopping Bot',
          text: 'Failed to stop the bot. Please try again.',
        });
        // setMessage('Error stopping bot');
      }
    };


    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
        {/* Greeting and Instructions */}
        <div className="bg-white w-full max-w-2xl p-6 border border-gray-300 rounded-md shadow-lg text-center">
          <h1 className="text-3xl font-bold mb-4">Hello, Lim Miin Ning!</h1>
          <p className="text-lg mb-6">
            Welcome to your dashboard. Here you can manage your profile and control the bot automation.
          </p>

          {/* User Profile */}
          <div className="bg-gray-100 p-4 rounded-lg mb-6">
            <h2 className="text-xl font-semibold mb-2">Profile Info</h2>
            <p><strong>Username:</strong> Lim Miin Ning</p>
          </div>
        <div className="space-x-4">
          {/* Edit Profile Button */}
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-md mb-4"
            onClick={() => window.location.href = '/edit-profile'}
          >
            Edit Profile
          </button>

          {/* Start/Stop Bot Button */}
          <button
            onClick={isBotRunning ? handleStopBot : handleStartBot}
            className={`text-white px-4 py-2 rounded-md ${isBotRunning ? 'bg-red-500' : 'bg-green-500'}`}
          >
            {isBotRunning ? 'Stop Bot' : 'Start Bot'}
          </button>
          </div>

          {/* Status Message */}
          {/* {message && <p className="mt-4 text-center">{message}</p>} */}
        </div>
    </div>
  );
};

export default Dashboard;