import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { db, auth } from '../../firebaseConfig';
import '../styles/UserDashboard.css';

const Dashboard = () => {
    const [isBotRunning, setIsBotRunning] = useState(false);
    const [username, setUsername] = useState('');
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    // const [message, setMessage] = useState('');

    // Capitalize the variable
    const capitalizeWords = (str) => {
      if (!str) return '';
      return str.split(' ').map(word => word[0].toUpperCase() + word.slice(1).toLowerCase( )).join(' ');
    }

    useEffect( () => {
      const unsubscribe = onAuthStateChanged(auth, async (user) => {
        if(user) {
          // Get user's UID
          const uid = user.uid;
          console.log('User is signed in:', uid);
          // Reference to the user's document in Firestore
          const studentDocRef = doc(db, 'students', uid);

          // Fetch user data from Firestore
          const studentDocSnap = await getDoc(studentDocRef);
          console.log('studentDocSnap:', studentDocSnap);
          if (studentDocSnap.exists()) {
            const studentData = studentDocSnap.data();
            setUsername(studentData.name);
          } else {
            console.log('No such document for user!');
            Swal.fire({
              icon: 'error',
              title: 'Error Fetching Data',
              text: 'Failed to fetch user data. Please try again.',
            });
          }
        } else if (!isLoggingOut) {   // Only show this alert when user attempts to turn to dashboard page without login
          console.log("User is signed out");
          Swal.fire({
            icon: 'error',
            title: 'You Are Not Signed In',
            text: 'Please sign in to access the dashboard.',
            timer: 1500,
            showConfirmButton: false,
            allowOutsideClick: false,
            // backdrop: true, // Dark backdrop with transparency
            // customClass: {
            //   backdrop: 'my-blurred-backdrop',  // Adjust backdrop opacity
            // }
          }).then(() => {
            Swal.fire({
              title: "Returning to login page...",
              timer: 1200,
              showConfirmButton: false,
              allowOutsideClick: false,
              // backdrop: true,  // Same dark backdrop
              customClass: {
                backdrop: 'my-blurred-backdrop',  // Adjust backdrop opacity
              },
              willClose: () => {
                // Redirect to login page after timer ends
                window.location.href = "/login";
              }
            });
          });
        } // end of if(user)
      }); // end of onAuthStateChanged

      return () => unsubscribe();
    }, [db, auth, isLoggingOut]);

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

    // Function to handle the logout
    const handleLogout = async () => {
      setIsLoggingOut(true);  // Set isLoggingOut to true when logging out
      // This is to let the system know the user just signed out, so not to use the onAuthStateChanged listener
      try {
        await signOut(auth);
        const timerDuration = 2000;
        Swal.fire({
          icon: 'success',
          title: 'Logged Out',
          html: `Redirecting in <b></b> seconds...`,
          timer: timerDuration,
          timerProgressBar: true,
          allowOutsideClick: false,
          // didOpen is triggered when the alert or modal is fully opened,
          // and it allows the user to interact with the aler
          didOpen: () => {
            Swal.showLoading();   // Show loading spinner
            const b = Swal.getHtmlContainer().querySelector('b');
            const interval = setInterval(() => {
              b.textContent = Math.ceil(Swal.getTimerLeft() / 1000);
            }, 100);

            // Clear the interval when the modal closes to avoid memory leaks
            Swal.getTimerLeft() <= 0 && clearInterval(interval);
          },
          willClose: () => {  
            window.location.href = '/login';  // Redirect to login page after logging out
          }
        });
        
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error Logging Out',
          text: 'An error occurred while logging out. Please try again.',
        })
      }

      // Alternative just like sign in
      // try {
        // Swal.fire({
          // icon: 'success',
          // title: 'Success',
          // text: 'Logged out successfully!',
          // showConfirmButton: false,
          // timer: 2200,
        // })
        // setTimeout(() => {
          // window.location.href = '/login'
        // }, 2500);   // Adjust delay slightly longer than the timer (2000ms)
      // } catch (error) {
        // console.error('Error logging out:', error);
        // setErrorMessage('An error occurred when signing out. Please try again.');
      // }
    };


    return (
        <div className="flex flex-col items-center justify-center h-screen">
        {/* Greeting and Instructions */}
        <div className="bg-white w-full max-w-2xl p-6 border border-gray-300 rounded-md shadow-lg text-center">
          <h1 className="text-3xl font-bold mb-4">Hello, {username? capitalizeWords(username) : 'User'}!</h1>
          <p className="text-lg mb-6">
            Welcome to your dashboard. Here you can manage your profile and control the bot automation.
          </p>

          {/* User Profile */}
          <div className="bg-gray-100 p-4 rounded-lg mb-6">
            <h2 className="text-xl font-semibold mb-2">Profile Info</h2>
            <p><strong>Username:</strong> {username? capitalizeWords(username) : 'User'}</p>
          </div>
        <div className="space-x-4">
          {/* Edit Profile Button */}
          <button
            className="bg-blue-500 hover:bg-blue-500 text-white px-4 py-2 rounded-md mb-4"
            onClick={() => window.location.href = '/editProfile'}
          >
            Edit Profile
          </button>

          {/* Start/Stop Bot Button */}
          <button
            onClick={isBotRunning ? handleStopBot : handleStartBot}
            className={`text-white px-4 py-2 rounded-md ${isBotRunning ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
          >
            {isBotRunning ? 'Stop Bot' : 'Start Bot'}
          </button>

          {/* Log Out Button */}
          <button
            onClick={handleLogout}
            className="bg-gray-500 hover:bg-red-600 text-white px-4 py-2 rounded-md"
          >
            Log Out
          </button>
          </div>

          {/* Status Message */}
          {/* {message && <p className="mt-4 text-center">{message}</p>} */}
        </div>
    </div>
  );
};

export default Dashboard;