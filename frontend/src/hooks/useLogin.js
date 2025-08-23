import { QueryClient, useMutation } from '@tanstack/react-query';
import React from 'react'
import { login } from '../lib/api';

const useLogin = () => {
  const {
     mutate: loginMutation,
     isPending,
     error,
   } = useMutation({
     mutationFn: login,
     onSuccess: () => QueryClient.invalidateQueries({ queryKey: ["authUser"] }),
   });

   return { error, isPending, loginMutation }
};

export default useLogin;