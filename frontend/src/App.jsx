import React from 'react'
import { Navigate, Route, Routes } from 'react-router'
import HomePage from "./pages/HomePage.jsx";
import SignUpPage from "./pages/SignUpPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import NotificationsPage from "./pages/NotificationsPage.jsx";
import CallPage from "./pages/CallPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import PageLoader from './components/PageLoader.jsx';
import useAuthUser from './hooks/useAuthUser.js';

const App = () => {
  const { isLoading, authUser } = useAuthUser();

  const isAuthenticated = Boolean(authUser);

  // Where does the authData come from???
  // const authUser = authData?.userWhichUsedInAppAndAuthRoute;
  if (isLoading) return <PageLoader />;

  return (
    <div className='h-screen' data-theme="aqua">
      <Routes>
        <Route path="/" element={ isAuthenticated ? <HomePage /> : <Navigate to="/login" /> } />
        <Route path="/signup" element={ !isAuthenticated ? <SignUpPage /> : <Navigate to="/" /> } />
        <Route path="/login" element={ !isAuthenticated ? <LoginPage /> : <Navigate to="/" /> } />
        <Route path="/notifications" element={ authUser ? <NotificationsPage /> : <Navigate to="/login" /> } />
        <Route path="/call" element={ isAuthenticated ? <CallPage /> : <Navigate to="/login" /> } />
        <Route path="/chat" element={ isAuthenticated ? <ChatPage /> : <Navigate to="/login" /> } />
      </Routes>

      <Toaster />
    </div>
  )
}

export default App