import React, { useState } from 'react';
import { signInWithEmailAndPassword, sendPasswordResetEmail } from 'firebase/auth';
import { auth } from '../../../firebaseConfig'; // Import the auth instance
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/20/solid';

const LoginComponent = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [resetEmail, setResetEmail] = useState(''); // For password reset email
  const [isResetVisible, setIsResetVisible] = useState(false); // To toggle reset email input
  const [showPassword, setShowPassword] = useState(false);  // To toggle password visibility

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      await signInWithEmailAndPassword(auth, email, password);
      window.location.href = '/dashboard'; // Redirect to dashboard on success
    } catch (error) {
      console.error('Error logging in:', error);
      setErrorMessage('Failed to log in. Email does not match the password.');
    }
  };

  const handlePasswordReset = async () => {
    try {
      await sendPasswordResetEmail(auth, resetEmail);
      alert('Password reset email sent! Check your inbox.');
      setIsResetVisible(false); // Hide reset email input after sending
    } catch (error) {
      console.error('Error sending reset email:', error);
      setErrorMessage('Failed to send reset email. Please try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        
        {/* Error Message */}
        {errorMessage && (
          <p className="text-red-500 mb-4 text-center">{errorMessage}</p>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div className="relative">
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            {/* Toggle Password Visibility */}
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute top-6 right-0 flex items-center p-2 text-gray-500"
            >
              {showPassword ? (
                <EyeIcon className="h-5 w-5" aria-hidden="true" />
              ) : (
                <EyeSlashIcon className="h-5 w-5" aria-hidden="true" />
              )}
            </button>
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Login
          </button>
        </form>

        {/* Forgot Password */}
        <p className="mt-4 text-sm text-center text-blue-500 hover:underline cursor-pointer" onClick={() => setIsResetVisible(!isResetVisible)}>
          Forgot Password?
        </p>

        {isResetVisible && (
          <div className="mt-4">
            <label htmlFor="resetEmail" className="block text-sm font-medium text-gray-700">Enter your email to reset password</label>
            <input
              type="email"
              id="resetEmail"
              value={resetEmail}
              onChange={(e) => setResetEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <button
              onClick={handlePasswordReset}
              className="mt-3 w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Reset Password
            </button>
          </div>
        )}

        <p className="mt-4 text-sm text-center">
          Don't have an account?{' '}
          <a href="/signup" className="text-blue-500 hover:underline">Register Here</a>
        </p>
      </div>
    </div>
  );
};

export default LoginComponent;
