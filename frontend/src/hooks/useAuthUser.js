import { useQuery } from '@tanstack/react-query';
import { getAuthUser } from '../lib/api.js';

// Axios
// React Query Tanstack query
const useAuthUser = () => {
    const authUser = useQuery({
    queryKey: ["authUser"],
    queryFn: getAuthUser,
    retry: false, // Auth check
  });

  // Question mark is just in case data is equal to undefined
  // todo: userWhichUsedInAppAndAuthRoute data?.userdaki user bu olabilir
  return { isLoading: authUser.isLoading, authUser: authUser.data?.userWhichUsedInAppAndAuthRoute };
}

export default useAuthUser