import { auth } from '../../../firebaseConfig'; // Ensure to import your Firebase auth instance

const LogoutComponent = () => {
  const handleSignOut = async () => {
    try {
      await auth.signOut(); // Sign out from Firebase
      window.location.href = '/login'; // Redirect to login page
    } catch (error) {
      console.error("Error signing out:", error); // Handle error
    }
  };

  return (
    <button onClick={handleSignOut}>
      Sign Out
    </button>
  );
};

export default LogoutComponent;
