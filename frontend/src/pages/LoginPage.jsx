import React, { useState } from 'react'
import { Link } from 'react-router';
import { PhoneCallIcon } from 'lucide-react';
import useLogin from '../hooks/useLogin.js';

const LoginPage = () => {
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
  });

  // This section is in the useLogin hook
  // const queryClient = useQueryClient();
  /*
  const {
    mutate: loginMutation,
    isPending,
    error,
  } = useMutation({
    mutationFn: login,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["authUser"] }),
  }); */

  const { isPending, error, loginMutation } = useLogin();

  const handleLogin = (e) => {
    e.preventDefault(), // Preventing the refresh
    loginMutation(loginData);
  };

  return (
    <div className="h-screen flex items-center justify-center p-4 sm:p-6 md:p-8" data-theme="valentine">
      <div className="border border-primary/25 flex flex-col lg:flex-row w-full max-w-5xl mx-auto bg-base-100
      rounded-xl shadow-lg overflow-hidden">
        {/* LOGIN FORM - LEFT SIDE */}
        <div className="w-full lg:w-1/2 p-4 sm:p-8 flex flex-col">
          {/* LOGO */}
          <div className="mb-4 flex items-center justify-start gap-2">
            <PhoneCallIcon className="size-9 text-primary" />
            <span className="text-3xl font-bold font-mono bg-clip-text text-transparent bg-gradient-to-r from-primary
            to-secondary tracking-wider">
              Tulululu
            </span>
          </div>

          {/* ERROR MESSAGE IF ANY */}
          { error && (
            <div className="alert alert-error mb-4">
              <span>{ error.response.data.message }</span>
            </div>
          )}

          <div className="w-full">
            <form onSubmit={ handleLogin }>
              <div className="space-y-4">
                {/* HEADER */}
                <div>
                  <h2 className="text-xl font-semibold">Login Your Account</h2>
                  <p className="text-sm opacity-70">
                    Welcome to Tulululu to call your lovers
                  </p>
                </div>

                {/* FILL IN PART */}
                <div className="space-y-3">
                  {/* GET THE EMAIL */}
                  <div className="form-control w-full">
                    <label className="label">
                      <span className="label-text">Email</span>
                    </label>
                    <input
                      type="email"
                      placeholder="orkinos@gmail.com"
                      className="input input-bordered w-full"
                      value={ loginData.email }
                      onChange={ (e) => setLoginData({ ...loginData, email: e.target.value })}
                      required
                    />
                  </div>

                  {/* GET THE PASSWORD */}
                  <div className="form-control w-full">
                    <label className="label">
                      <span className="label-text">Password</span>
                    </label>
                    <input
                      type="password"
                      placeholder="******"
                      className="input input-bordered w-full"
                      value={ loginData.password }
                      onChange={ (e) => setLoginData({ ...loginData, password: e.target.value })}
                      required
                    />
                  </div>
                </div>

                {/* LOGIN BUTTON */}
                <button className="btn btn-primary w-full" type="submit">
                  {isPending ? (
                    <>
                      <span className="loading loading-spinner loading-xs"></span>
                      Signing in...
                    </>
                  ) : (
                    "Login"
                  )}
                </button>

                {/* DONT YOU HAVE AN ACCOUNT */}
                <div className="text-center mt-4">
                  <p className="text-sm">
                    Create an Account{" "}
                    <Link to="/signup" className="text-primary hover:underline">
                      Signup
                    </Link>
                  </p>
                </div>
              </div>
            </form>
          </div>
        </div>

        {/* SIGNUP FORM - RIGHT SIDE - WITH THE PHOTO */}
        <div className="hidden lg:flex w-full lg:w-1/2 bg-primary/10 items-center justify-center">
          <div className="max-w-md p-8">
            {/* ILLUSTRATION */}
            <div className="relative aspect-square max-w-sm mx-auto">
              <img src="/video_call.png" alt="Video Calling Illustration" className="w-full h-full" />
            </div>

            <div className="text-center spacec-y-3 mt-6">
              <h2 className="text-xl font-semibold">Connect with your lovely friends</h2>
              <p className="opacity-70">
                Add your friends and Start to talk without using VPN like for accessing  banned apps or Pay-to-Call like fckng Zoom
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};


export default LoginPage