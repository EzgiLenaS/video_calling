import React from 'react'
import { Route, Routes } from 'react-router'
import HomePage from "./pages/HomePage.jsx";
import SignUpPage from "./pages/SignUpPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import NotificationsPage from "./pages/NotificationsPage.jsx";
import CallPage from "./pages/CallPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import toast, { Toaster } from 'react-hot-toast';

const App = () => {
  return (
    <div className='h-screen' data-theme="aqua">
      <Routes>
        <Route path="/" element={ <HomePage /> } />
        <Route path="/signup" element={ <SignUpPage /> } />
        <Route path="/login" element={ <LoginPage /> } />
        <Route path="/notifications" element={ <NotificationsPage /> } />
        <Route path="/call" element={ <CallPage /> } />
        <Route path="/chat" element={ <ChatPage /> } />
      </Routes>
      <button className="btn" onClick={() => toast.success("HelloWorld!")}>Create a Toast</button>
      <button className="btn btn-neutral">Neutral</button>
      <button className="btn btn-primary">Primary</button>
      <button className="btn btn-secondary">Secondary</button>
      <button className="btn btn-accent">Accent</button>
      <button className="btn btn-ghost">Ghost</button>
      <button className="btn btn-link">Link</button>

      <Toaster />
    </div>
  )
}

export default App