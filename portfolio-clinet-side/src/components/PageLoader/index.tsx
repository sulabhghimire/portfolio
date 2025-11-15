import { Suspense, type JSX } from "react";

interface IPageLoaderProps{
    children: JSX.Element,
    fallback?: JSX.Element
}

const DefaultFallBack = () => {
    return <div className="p-8">Loading…</div>
}


function PageLoader({ children, fallback }: IPageLoaderProps) {
  const fallbackComponent = fallback || <DefaultFallBack/>

  return <Suspense fallback={fallbackComponent}>{children}</Suspense>;
}

export default PageLoader;