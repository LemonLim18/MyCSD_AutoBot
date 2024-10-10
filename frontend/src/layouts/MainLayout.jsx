// src/layouts/MainLayout.jsx
import React from 'react';
import { UserProvider } from '../components/UserContext';

const MainLayout = ({ children }) => {
  return (
    <UserProvider>
      {children}
    </UserProvider>
  );
};

export default MainLayout;