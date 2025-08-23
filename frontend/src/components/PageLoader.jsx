import { LoaderIcon } from 'lucide-react'
import React from 'react'

const PageLoader = () => {
  return (
    <div className='min-h-screen flex item-center justify-center'>
        <LoaderIcon className='animate-spin size-10 text-primary' />
    </div>
  )
}

export default PageLoader