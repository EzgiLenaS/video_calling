import { Navigate, Route, Routes } from 'react-router'

import HomePage from "./pages/HomePage.jsx";
import SignUpPage from "./pages/SignUpPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import NotificationsPage from "./pages/NotificationsPage.jsx";
import CallPage from "./pages/CallPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";


import Layout from "./components/Layout.jsx";
import { useThemeStore } from "./store/useThemeStore.js";
import useAuthUser from './hooks/useAuthUser.js';
import PageLoader from './components/PageLoader.jsx';

import { Toaster } from "react-hot-toast";

const App = () => {
  const { isLoading, authUser } = useAuthUser();

  const isAuthenticated = Boolean(authUser);
  const { theme } = useThemeStore();

  // Where does the authData come from???
  // const authUser = authData?.userWhichUsedInAppAndAuthRoute;
  if (isLoading) return <PageLoader />;

  return (
    <div className="h-screen" data-theme={theme}>
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Layout showSidebar={true}>
                <HomePage />
              </Layout>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route path="/signup" element={ !isAuthenticated ? (<SignUpPage />) : (<Navigate to="/" />) } />
        <Route path="/login" element={ !isAuthenticated ? (<LoginPage />) : (<Navigate to="/" />) } />
        <Route
          path="/notifications"
          element={
            authUser ? (
              <Layout showSidebar={true}>
                <NotificationsPage />
              </Layout>
              ) : (
              <Navigate to="/login" />
              ) 
            }
        />
        <Route path="/call" element={ isAuthenticated ? (<CallPage />) : (<Navigate to="/login" />) } />
        <Route
          path="/chat"
          element={
            isAuthenticated ? (
              <Layout showSidebar={false}>
                <ChatPage />
              </Layout>
              ) : (
              <Navigate to="/login" />
              )
            }
        />
      </Routes>

      <Toaster />
    </div>
  )
}

export default App